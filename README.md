# Cleansio

[![Build Status](https://travis-ci.com/PatrickDuncan/cleansio.svg?token=9iihWUtXPiNNfbJx3N13&branch=master)](https://travis-ci.com/PatrickDuncan/cleansio)

## Usage
```
python cleansio.py <FLAC_PATH>
```
- FLAC_PATH
    - Must be a .flac audio file
    - It must be mono (as opposed to stereo)
    - Must be less than 10 seconds
    - The sample rate must be 44100

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
7. _(OPTIONAL)_ Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/)
8. You're all set!

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
