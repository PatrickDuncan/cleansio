# Cleansio

[![Build Status](https://travis-ci.com/PatrickDuncan/cleansio.svg?token=9iihWUtXPiNNfbJx3N13&branch=master)](https://travis-ci.com/PatrickDuncan/cleansio) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<img src="assets/logo.png" width="400px" alt="logo">

## Usage
```
python cleansio/cleansio.py <FILE_PATH>
```

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

## Docker

**Run**
```
docker run \
  --tty \
  --rm \
  --volume <PATH_TO_MUSIC>:/music \
  --volume <PATH_TO_GOOGLE_CLOUD_SPEECH_JSON>:/google-cloud-speech-api.json \
  --name cleansio \
  patrickduncan/cleansio \
  /music/<MUSIC_FILE_NAME>
```

**Build**
```
docker build --tag "cleansio:dev" .
```

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
| [<img src="https://avatars.githubusercontent.com/u/6889074?v=3" width="100px;"/><br /><sub><b>Patrick D. Duncan</b></sub>](https://patrickduncan.co)<br /> [💻](https://github.com/patrickduncan/cleansio/commits?author=patrickduncan) [🚇](https://travis-ci.com/PatrickDuncan/cleansio) 📖 | [<img src="https://avatars.githubusercontent.com/u/11710526?v=3" width="100px;"/><br /><sub><b>Levin Noronha</b></sub>](https://github.com/levin-noro)<br /> [💻](https://github.com/patrickduncan/cleansio/commits?author=levin-noro) | [<img src="https://avatars.githubusercontent.com/u/15528033?v=3" width="100px;"/><br /><sub><b>Corie Bain</b></sub>](https://github.com/c-bain)<br /> [💻](https://github.com/patrickduncan/cleansio/commits?author=c-bain) | [<img src="https://avatars.githubusercontent.com/u/1454713?v=3" width="100px;"/><br /><sub><b>Victor Carri</b></sub>](https://github.com/VictorCarri)<br /> [💻](https://github.com/patrickduncan/cleansio/commits?author=VictorCarri) 📖 | [<img src="https://avatars.githubusercontent.com/u/35604837?v=3" width="100px;"/><br /><sub><b>Richard Caseres</b></sub>](https://github.com/richardbmx)<br />[🎨](https://github.com/PatrickDuncan/cleansio/blob/logo/assets/logo.png) |
| :---: | :---: | :---: | :---: | :---: |
<!-- ALL-CONTRIBUTORS-LIST:END -->
