FROM amazonlinux:2

WORKDIR /tmp

RUN yum -y update \
    && yum -y install gcc-c++ findutils tar gzip glibc

RUN touch ~/.bashrc && chmod +x ~/.bashrc

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash

RUN source ~/.bashrc \
    && nvm install 18

WORKDIR /build

RUN source ~/.bashrc \
    && npm init -f -y \
    && npm install querystring --save \
    && npm install request --save \
    && npm install --only=prod \
    && cd build && rm -rf node_modules/sharp
    && zip -r9q /lambda.zip *
