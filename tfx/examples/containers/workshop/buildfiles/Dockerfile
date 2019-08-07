FROM ubuntu:16.04
LABEL maintainer="robertcrowe@google.com"

COPY init.sh /

RUN apt-get update && apt-get install -y --no-install-recommends \
        apt-utils \
        python-pip \
        python3-pip \
        python3-dev \
        virtualenv \
        git \
        sudo \
        build-essential \
        software-properties-common \
        && apt-get autoclean \
        && apt-get autoremove --purge \
        && chmod +x /init.sh \
        && bash /init.sh

EXPOSE 8080 8888
