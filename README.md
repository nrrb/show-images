how-images
===========

A Flask app that takes a URL, finds all the images referred to in the page found at that URL, and displays just the images.

Request format:

    http://show-images/?key=KillDecimal10&url=http://dirigible-iceskates.biz/

Where the `key` parameter in the URL matches the `SHOW_IMAGES_KEY` in `config.py`. 

# Getting Started

Create a virtual environment and install the requirements.

```
mkvirtualenv show-images
pip install -r requirements.txt
```

Copy `config.py.template` to `config.py` and change this value to a special string, and choose the path of the SQLite database file.

Create the database file.

```
python createdb.py
```

Run the application server.

```
python app.py
```

Go to http://127.0.0.1:5000/?key=&url=http://www.google.com/ with your key substituted in.

# Built on the shoulders of giants

This wouldn't be possible without the Python web micro-framework [Flask](http://flask.pocoo.org/), [requests](http://docs.python-requests.org/en/latest/) for dead simple HTTP requests, and [beautifulsoup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/) and for dead simple HTML scraping.

Thanks to [Dan on StackOverflow](http://stackoverflow.com/a/169631) for his basic regular expression for matching image URLs. 

This looks decent because of Bootstrap Zero's MIT-licensed [Landing Page Bootstrap Theme](http://bootstrapzero.com/bootstrap-template/landing-page).

I then meddled with a good thing by dumping in some icons from [Font Awesome](http://fortawesome.github.io/Font-Awesome/) and buttons from Twitter's [Bootstrap](http://getbootstrap.com/) CSS framework.
