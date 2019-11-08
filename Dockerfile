FROM python:3.7-alpine
MAINTAINER Riszky Maulana "riszky@biznetgio.com"
RUN apk add --no-cache bash
RUN apk add --no-cache curl
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR /code
RUN mkdir /code/log
COPY . /code
RUN apk add --no-cache tzdata
ENV TZ Asia/Jakarta
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "bash", "/entrypoint.sh" ]