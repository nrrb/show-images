# Standard Library
from datetime import datetime
import os
import re
from urlparse import urljoin
# Third Party Imports
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import requests
# Local Imports
from config import SECRET_KEY

# Regex from http://stackoverflow.com/a/169631
image_url_pattern = (r'https?://(?:[a-z\-]+\.)+[a-z]{2,6}'
                     r'(?:/[^/#?]+)+\.(?:jpg|gif|png)')

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

class PageCache(db.Model):
    url = db.Column(db.String(500), primary_key=True)
    html = db.Column(db.Text)
    created = db.Column(db.DateTime)

    def __init__(self, url, html):
        self.url = url
        self.html = html
        self.created = datetime.now()


def get_image_urls_from_html(html, base_url=None):
    # Search by regular expression first
    image_urls = re.findall(image_url_pattern, html)
    # Then use BeautifulSoup to extract those pesky image tags
    soup = BeautifulSoup(html)
    imgs = soup.findAll('img')
    image_urls += list(set(filter(lambda a: a,
            [img.attrs.get('src') for img in imgs])))
    # Sometimes there's an interesting data-rollover on images
    image_urls += list(set(filter(lambda a: a, 
            [img.attrs.get('data-rollover') for img in imgs])))
    if base_url is not None:
        image_urls = [urljoin(base_url, url) for url in image_urls]
    return sorted(image_urls)


@app.route('/', methods=['GET'])
def index():
    key = request.args.get('key')
    url = request.args.get('url')
    if key and url and key == SECRET_KEY:
        cache = db.session.query(PageCache).filter_by(url=url).first()
        if cache:
            html = cache.html
        else:
            response = requests.get(url)
            html = response.content
            cache = PageCache(url, html)
            db.session.add(cache)
            db.session.commit()
        retrieval_date = datetime.isoformat(cache.created)
        image_urls = get_image_urls_from_html(html, base_url=url)
        return render_template('index.html', url=url, 
            image_urls=image_urls, retrieval_date=retrieval_date)
    else:
        return 'o_O'

if __name__ == '__main__':
    app.run(debug=True)
