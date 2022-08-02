# Image Scraper
This algorithm is aimed to be utilized as part of the backend for the Object Detection project.
It takes two arguments, a keyword and request number. The algorithm searches the keyword from google images, 
scrapes the provided number of images, converts the images to an array of blobs, and returns the array. 

## The Source Code
The src code for this project is found in the [app](./app) directory; [app.py](./app/app.py)
the actual scraping happens in [scraper](./app/scraper).

## Note
Make sure to run 
```
pip3 install -r requirements.txt
```
to install the necessary modules.