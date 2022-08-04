# Image Scraper
This algorithm is aimed to be utilized as part of the backend for the Object Detection project.
It takes two arguments, a keyword and request number. The algorithm searches the keyword from google images, 
scrapes the provided number of images, converts the images to an array of blobs, and returns the array. 

## The Source Code
The src code for this project is found in the [app](./app) directory; [app.py](./app/app.py)
the actual scraping happens in [scraper](./app/scraper).

## Dockerize the app and run locally
Go to the Dockerfile's directory in the terminal and issue these commands:
```
docker build -t image-scraper-fargate-container .
```
and 
```
docker run -p 9000:8080 image-scraper-fargate-container
```
'image-scraper-fargate-container' will be the name of the created image and can be replaced with any other name.

## Note
Make sure to run 
```
pip3 install -r requirements.txt
```
to install the necessary modules.

## Push the docker image to ECR
Connect docker client with AWS ECR (be sure to replace the region and AWS account ID with your own):
```
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 190047048560.dkr.ecr.ap-northeast-2.amazonaws.com
```
Obtain the ID of the image that you are trying to push:
```
docker images
```
Tag the image using its ID:
```
docker tag d8a3b74c72ca 190047048560.dkr.ecr.ap-northeast-2.amazonaws.com/image-scraping-repo:latest
```
and finally push it to ECR:
```
docker push 190047048560.dkr.ecr.ap-northeast-2.amazonaws.com/image-scraping-repo:latest
```