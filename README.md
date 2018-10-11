# Cleansio

[![Build Status](https://travis-ci.com/PatrickDuncan/cleansio.svg?token=9iihWUtXPiNNfbJx3N13&branch=master)](https://travis-ci.com/PatrickDuncan/cleansio) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Usage
```
python cleansio/cleansio.py <FILE_PATH>
```
- FILE_PATH
    - It must be mono (as opposed to stereo)

### Requirements

1. Posix shell

## Setup

1. Check the Requirements
2. Clone this repo
3. Install Python 3.4+
    - [Anaconda is recommended](https://www.anaconda.com/download/)
4. Download your Google Cloud Credentials JSON file
5. Set the following environment variables:
    ```
    export GOOGLE_APPLICATION_CREDENTIALS=<PATH_TO_JSON>
    ```
6. Install the following Python libraries:
    ```
    pip install --upgrade google-cloud-speech
    ```
7. If you're using _macOS_ or _Windows_ follow these [**additional steps**](https://github.com/ahupp/python-magic#windows). Then install:
    ```
    pip install python-magic
    ```
8. Follow these [**additional steps**](https://github.com/jiaaro/pydub#getting-ffmpeg-set-up) and then install:
    ```
    pip install pydub
    ```
9. _(OPTIONAL)_ Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/)
10. You're all set!

## Developer Setup

1. Follow Setup
2. Install the following Python libraries:
    ```
    pip install --upgrade pylint
    ```

### Linting

**Run**
```
./bin/lint
```

**Help**
```
pylint --help-msg=<ID>
```
