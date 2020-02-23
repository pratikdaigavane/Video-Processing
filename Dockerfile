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

RUN apk del .build-deps
RUN apk add --no-cache mariadb-connector-c-dev

# Copying app to docker and making it as working directory
RUN mkdir /app
WORKDIR /app
COPY ./app /app

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait
# Creating a user and switching to it(for security)
RUN adduser -D user
USER user

