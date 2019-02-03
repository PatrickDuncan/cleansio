# Cleansio

[![Build Status](https://travis-ci.com/PatrickDuncan/cleansio.svg?token=9iihWUtXPiNNfbJx3N13&branch=master)](https://travis-ci.com/PatrickDuncan/cleansio) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Documentation Status](https://readthedocs.org/projects/cleansio/badge/?version=latest)](https://cleansio.readthedocs.io/en/latest/?badge=latest)


<img src="media/logo.png" width="200px" alt="logo">

## Usage

```sh
python cleansio/cleansio.py --help
```

### Requirements

1. Posix shell
2. Internet connection

## Setup

1. Check the Requirements
2. Clone this repo
3. Install Python 3.4+
    - [Anaconda is recommended](https://www.anaconda.com/download/)
4. Download your Google Cloud Credentials JSON file
5. Set the following environment variables:
    ```sh
    export GOOGLE_APPLICATION_CREDENTIALS=<PATH_TO_JSON>
    ```
6. Follow these additional steps:
    - [ffmpeg set-up](https://github.com/jiaaro/pydub#getting-ffmpeg-set-up)
7. Install Cleansio's dependencies:
    ```sh
    pip install -r requirements.txt
    ```
8. _(OPTIONAL)_ If you're a developer run:
    ```sh
    pip install -r requirements-dev.txt
    ```
9. _(OPTIONAL)_ Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/)
10. You're all set!

## Documentation

[Technical Documentation](https://patrickdduncan.com/cleansio)

[Slideshow](https://patrickdduncan.com/clenasio-slideshow)

**Build Locally.** Available at _docs/\_build/html/index.html_
```sh
./bin/generate_docs
```

### Linting

**Run**
```sh
./bin/lint
```

**Help**
```sh
pylint --help-msg=<ID>
```

### Testing

```sh
./bin/test
```

## Docker

**Run**
```sh
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
```sh
docker build --tag "cleansio:dev" .
```

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
| [<img src="https://avatars.githubusercontent.com/u/6889074?v=3" width="100px;"/><br /><sub><b>Patrick D. Duncan</b></sub>](https://patrickduncan.co)<br /> [💻](https://github.com/patrickduncan/cleansio/commits?author=patrickduncan) | [<img src="https://avatars.githubusercontent.com/u/11710526?v=3" width="100px;"/><br /><sub><b>Levin Noronha</b></sub>](https://github.com/levin-noro)<br /> [💻](https://github.com/patrickduncan/cleansio/commits?author=levin-noro) | [<img src="https://avatars.githubusercontent.com/u/15528033?v=3" width="100px;"/><br /><sub><b>Corie Bain</b></sub>](https://github.com/c-bain)<br /> [💻](https://github.com/patrickduncan/cleansio/commits?author=c-bain) | [<img src="https://avatars.githubusercontent.com/u/1454713?v=3" width="100px;"/><br /><sub><b>Victor Carri</b></sub>](https://github.com/VictorCarri)<br /> [💻](https://github.com/patrickduncan/cleansio/commits?author=VictorCarri) |
| :---: | :---: | :---: | :---: |
<!-- ALL-CONTRIBUTORS-LIST:END -->
