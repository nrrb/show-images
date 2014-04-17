# Standard Library
import codecs
from datetime import datetime
import os
import re
from urlparse import urljoin
# Third Party Imports
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import requests


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


class image_urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_url = db.Column(db.String(500))
    image_url = db.Column(db.String(500))

    def __init__(self, page_url, image_url):
        self.page_url = page_url
        self.image_url = image_url


def get_image_urls_from_html(html, base_url=None):
    # Search by regular expression first
    urls = re.findall(image_url_pattern, html)
    # Then use BeautifulSoup to extract those pesky image tags
    soup = BeautifulSoup(html)
    imgs = soup.findAll('img')
    urls += list(set(filter(lambda a: a,
            [img.attrs.get('src') for img in imgs])))
    # Sometimes there's an interesting data-rollover on images
    urls += list(set(filter(lambda a: a,
            [img.attrs.get('data-rollover') for img in imgs])))
    if base_url is not None:
        urls = [urljoin(base_url, url) for url in urls]
    return sorted(list(set(urls)))


def get_url(url):
    cache = db.session.query(PageCache).filter_by(url=url).first()
    if cache:
        html = cache.html
    else:
        response = requests.get(url)
        html = response.text
        cache = PageCache(url, html)
        db.session.add(cache)
        db.session.commit()
    return html


@app.route('/', methods=['GET'])
def index():
    url = request.args.get('url')
    if url:
        html = get_url(url)
        urls = get_image_urls_from_html(html, base_url=url)
        return render_template('index.html', url=url, image_urls=urls)
    else:
        return 'o_O'


@app.route('/urls', methods=['GET'])
def urls():
    url = request.args.get('url')
    show_links = (request.args.get('show_links') == 'on')
    show_images = (request.args.get('show_images') == 'on')
    if url:
        html = get_url(url)
        urls = get_image_urls_from_html(html, base_url=url)
        for image_url in urls:
            url_cache = image_urls(page_url=url, image_url=image_url)
            db.session.add(url_cache)
            db.session.commit()
        return render_template('urls.html', urls=urls,
            show_links=show_links, show_images=show_images)
    else:
        return render_template('get_urls.html')


@app.route('/history', methods=['GET'])
def history():
    urls = [item.url for item in db.session.query(PageCache).all()]
    return render_template('history.html', urls=urls)


@app.route('/paste', methods=['GET', 'POST'])
def paste():
    if request.method=='GET':
        return render_template('paste.html')
    else:
        url = request.form['url']
        html = request.form['html']
        urls = get_image_urls_from_html(html, base_url=url)
        return render_template('index.html', url=url, image_urls=urls)


if __name__ == '__main__':
    app.run(debug=True)
