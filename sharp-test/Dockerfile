# FROM public.ecr.aws/lambda/nodejs:18

# # Exec commands
# COPY index.js ${LAMBDA_TASK_ROOT}

# # Commands
# # RUN npm cache clean --force && rm -rf node_modules

# ## update the dockerfile with the following lines:
# RUN yum -y update && yum -y install zip \
#     && npm init -f -y \
#     && npm install querystring --save \
#     && npm install request --save \
#     && npm install --only=prod \
#     && SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install --arch=x64 --platform=linux sharp \
#     && zip -r9q /lambda.zip *

# CMD ["index.handler"]

FROM amazonlinux:2

WORKDIR /tmp

RUN yum -y update \
    && yum -y install gcc-c++ findutils tar gzip glibc

RUN touch ~/.bashrc && chmod +x ~/.bashrc

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash

RUN source ~/.bashrc \
    && nvm install 18

WORKDIR /build

# COPY index.js .

# RUN source ~/.bashrc && yum -y update && yum -y install gcc-c++ make nodejs && npm init -f -y \
#     && npm install querystring --save \
#     && npm install request --save \
#     && npm install --only=prod \
#     && SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install --arch=x64 --platform=linux sharp \
#     && zip -r9q /lambda.zip *
