FROM python:3.4

USER root
WORKDIR /root

COPY cleansio cleansio

#===============================================================================
# Install Libraries
#===============================================================================
RUN apt-get update &&  \
  apt-get -qqy install \
  # For pydub
  libav-tools          \
  libavcodec-extra

RUN pip install --upgrade \
  google-cloud-speech     \
  pydub

#===============================================================================
# Set Google Speech API
#===============================================================================
ENV GOOGLE_APPLICATION_CREDENTIALS=/google-cloud-speech-api.json

#===============================================================================
# Execute cleansio
#===============================================================================
ENTRYPOINT ["python", "cleansio/cleansio.py"]
