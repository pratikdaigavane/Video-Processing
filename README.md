# Video-Processing

> Screening task for FOSSEE Summer Fellowship
>
[![Build Status](https://travis-ci.com/pratikdaigavane/Video-Processing.svg?token=n9GNM7C4LryMEo4g1p51&branch=master)](https://travis-ci.com/pratikdaigavane/Video-Processing)

Django application that allows a user to upload a video and its .srt file containing subtitles. The video is broken into chunks, based on the timing information specified in the .srt file. The corresponding audio is extracted from each video chunk and stored is separately.

For the uploaded video, the start time, end time, video chunk sequence number, subtitles, and its respective audio (.mp3) are shown. For each audio, there is facility to ‘Upload’, in which a user is allowed to re-upload the edited .mp3 file for that video chunk. The ‘Download tutorial’ button will combine all the video chunks with respective audio chunks into single video (.mp4 file).

![](header.png)

## Starting Server

Docker Compose
```sh
docker-compose up
```

Windows:

```sh
edit autoexec.bat
```

## Usage example

A few motivating and useful examples of how your product can be used. Spice this up with code blocks and potentially more screenshots.

_For more examples and usage, please refer to the [Wiki][wiki]._

## Development setup

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
make install
npm test
```

## Release History

* 0.2.1
    * CHANGE: Update docs (module code remains unchanged)
* 0.2.0
    * CHANGE: Remove `setDefaultXYZ()`
    * ADD: Add `init()`
* 0.1.1
    * FIX: Crash when calling `baz()` (Thanks @GenerousContributorName!)
* 0.1.0
    * The first proper release
    * CHANGE: Rename `foo()` to `bar()`
* 0.0.1
    * Work in progress

## Meta

Your Name – [@YourTwitter](https://twitter.com/dbader_org) – YourEmail@example.com

Distributed under the XYZ license. See ``LICENSE`` for more information.

[https://github.com/yourname/github-link](https://github.com/dbader/)

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki
