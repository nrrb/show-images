show-images
===========

A Flask app that takes a URL, finds all the images referred to in the page found at that URL, and displays just the images.

Request format:

    http://show-images/?key=KillDecimal10&url=http://dirigible-iceskates.biz/

Where the `key` parameter in the URL matches the `SHOW_IMAGES_KEY` environment variable you must set:

```
export SHOW_IMAGES_KEY=KillDecimal10
```
