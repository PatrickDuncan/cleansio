FROM python:3.4

USER root
WORKDIR /root

COPY . cleansio

#===============================================================================
# Install Libraries
#===============================================================================
RUN apt-get update &&  \
  apt-get -qqy install \
  # For pydub
  libav-tools          \
  libavcodec-extra

WORKDIR cleansio

RUN pip install -r requirements.txt

#===============================================================================
# Set Google Speech API
#===============================================================================
ENV GOOGLE_APPLICATION_CREDENTIALS=/google-cloud-speech-api.json

#===============================================================================
# Execute cleansio
#===============================================================================
ENTRYPOINT ["python", "cleansio/cleansio.py"]
