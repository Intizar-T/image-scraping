FROM python:3.9

# # install google chrome
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# RUN apt-get -y update --fix-missing
# RUN apt-get install -y google-chrome-stable

# # install chromedriver
# RUN apt-get install -yqq unzip
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

# Install requirements first so this step is cached by Docker
COPY /requirements.txt /home/image-scraper-fargate-container/requirements.txt
WORKDIR /home/image-scraper-fargate-container/
RUN pip install -r requirements.txt

# copy code
COPY app /home/image-scraper-fargate-container/app/


# # Define global args
# ARG FUNCTION_DIR="/home/app/"
# ARG RUNTIME_VERSION="3.9"
# ARG DISTRO_VERSION="3.12"


# # Stage 1 - bundle base image + runtime
# # Grab a fresh copy of the image and install GCC
# FROM python:${RUNTIME_VERSION}-alpine${DISTRO_VERSION} AS python-alpine
# # Install GCC (Alpine uses musl but we compile and link dependencies with GCC)
# RUN apk add --no-cache \
#     libstdc++


# # Stage 2 - build function and dependencies
# FROM python-alpine AS build-image

# # Include global args in this stage of the build
# ARG FUNCTION_DIR
# ARG RUNTIME_VERSION
# # Create function directory
# RUN mkdir -p ${FUNCTION_DIR}


# # Stage 3 - Add app related dependencies
# FROM python-alpine as build-image2
# ARG FUNCTION_DIR
# WORKDIR ${FUNCTION_DIR}
# # Copy in the built dependencies
# COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
# # Copy over and install requirements
# RUN apk update \
#     && apk add gcc python3-dev musl-dev \
#     && apk add jpeg-dev zlib-dev libjpeg-turbo-dev
# COPY requirements.txt .
# RUN python${RUNTIME_VERSION} -m pip install -r requirements.txt --target ${FUNCTION_DIR}


# # Stage 4 - final runtime image
# # Grab a fresh copy of the Python image
# FROM python-alpine
# ARG FUNCTION_DIR
# WORKDIR ${FUNCTION_DIR}
# # Copy in the built dependencies
# COPY --from=build-image2 ${FUNCTION_DIR} ${FUNCTION_DIR}
# RUN apk add jpeg-dev zlib-dev libjpeg-turbo-dev \
#     && apk add chromium chromium-chromedriver
    
# COPY app/* ${FUNCTION_DIR}
# COPY entry.sh /
# ENTRYPOINT [ "/entry.sh" ]
# CMD [ "app.handler" ]