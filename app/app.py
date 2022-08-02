from scraper.scraper import ImageScraper
from PIL import Image
import io

def handler(event, context=None):
    scr = ImageScraper()
    urls = scr.get_image_urls(query=event['query'], max_urls=event['count'], sleep_between_interactions=1)
    files = []
    for url in urls:
        img_obj = scr.get_in_memory_image(url, 'jpeg')
        files.append(img_obj)
    
    # print(len(files))
    # image1 = io.BytesIO(files[0])
    # image150 = io.BytesIO(files[1])
    # image300 = io.BytesIO(files[2])
    # Image.open(image1).convert('RGB').show()
    # Image.open(image150).convert('RGB').show()
    # Image.open(image300).convert('RGB').show()
    
    
    scr.close_connection()
    return "Successfully loaded {} images and file names {}.".format(event['count'], files)

def main():
    event = { 'query': 'ant', 'count': 3 }
    handler(event)

if __name__ == '__main__':
    main()