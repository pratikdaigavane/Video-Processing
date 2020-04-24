# Video-Processing

> Screening task for FOSSEE Summer Fellowship
>
[![Build Status](https://travis-ci.com/pratikdaigavane/Video-Processing.svg?token=n9GNM7C4LryMEo4g1p51&branch=master)](https://travis-ci.com/pratikdaigavane/Video-Processing)
[![Code Factor](https://www.codefactor.io/repository/github/pratikdaigavane/Video-Processing/badge?style=plastic)](https://www.codefactor.io/repository/github/pratikdaigavane/Video-Processing)


Django application that allows a user to upload a video and its .srt file containing subtitles. The video is broken into chunks, based on the timing information specified in the .srt file. The corresponding audio is extracted from each video chunk and stored is separately.

For the uploaded video, the start time, end time, video chunk sequence number, subtitles, and its respective audio (.mp3) are shown. For each audio, there is facility to ‘Upload’, in which a user is allowed to re-upload the edited .mp3 file for that video chunk. The ‘Download tutorial’ button will combine all the video chunks with respective audio chunks into single video (.mp4 file).

## Demo Video
[![FOSSEE Video Processing](https://pratikdaigavane.github.io/fosee2.png)](https://www.youtube.com/watch?v=NMdinGKIyn8 
"FOSSEE Video Processing")

![](https://pratikdaigavane.github.io/fosse1.png)

## Highlights of the Project
* PEP-8 Coding guidelines followed
* Celery and RabbitMQ to make project asynchronous
* Docker used to containerize the project
* Backend hosted on Django Server
* Frontend hosted on Nginx Server
* Travis CI used for continuous integration

## Prerequisites
This project is built on top of docker containers. 
So ensure that you have Docker and Docker Compose installed on your system
For installation instructions refer: https://docs.docker.com/install/

## Running unit test cases
* This project follows TDD(Test Drive Development) style.
* Flake8 is used as primary linter for the project

To run test cases:
```sh
docker-compose run app sh -c "python manage.py test && flake8"
```

## Starting the Server

Start the MySQL database first:
```sh
docker-compose up db
```
Then start whole project:
```sh
docker-compose up
```
Now the backend will be hosted at 127.0.0.1:8000
and the frontend will be hosted at 127.0.0.1

## API Documentation
API documentation is done using swagger
visit https://pratikdaigavane.github.io/ for API documentation 
