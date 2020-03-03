FROM python:3.8-alpine
MAINTAINER Pratik Daigavane

#Run python in unbuffered mode to allow for log messages to be
#immediately dumped to the stream instead of being buffered.
ENV PYTHONUNBUFFERED 1

RUN set -e; \
        apk add --no-cache --virtual .build-deps \
                gcc \
                libc-dev \
                linux-headers \
                mariadb-dev \
                python3-dev \
        ;

# Install all dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
RUN apk add ffmpeg
RUN apk del .build-deps
RUN apk add --no-cache mariadb-connector-c-dev

# Copying app to docker and making it as working directory
RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user

