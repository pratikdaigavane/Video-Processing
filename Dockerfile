FROM python:3.8-alpine
MAINTAINER Pratik Daigavane

#Run python in unbuffered mode to allow for log messages to be
#immediately dumped to the stream instead of being buffered.
ENV PYTHONUNBUFFERED 1

# Install all dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# Copying app to docker and making it as working directory
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# Creating a user and switching to it(for security)
RUN adduser -D user
USER user
