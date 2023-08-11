# FROM public.ecr.aws/lambda/python:3.9

# # general build stuff
# RUN yum update -y \
# 	&& yum groupinstall -y "Development Tools" \
# 	&& yum install -y wget tar gcc-c++ pkgconfig glib2 glib2-devel expat-devel python3-devel -y

# # libvips needs libwebp 0.5 or later and the one on amazonlinux2 is 0.3.0, so
# # we have to build it ourselves

# # packages needed by libwebp
# RUN yum install -y \
# 	libjpeg-devel \
# 	libpng-devel \
# 	libtiff-devel \
# 	libgif-devel 

# # stuff we need to build our own libvips ... this is a pretty basic selection
# # of dependencies, you'll want to adjust these
# # dzsave needs libgsf
# RUN yum install -y \
# 	libpng-devel \
# 	poppler-glib-devel \
# 	glib2-devel \
# 	libjpeg-devel \
# 	expat-devel \
# 	zlib-devel \
# 	orc-devel \
# 	lcms2-devel \
# 	libexif-devel \
# 	libgsf-devel

# # openslide is in epel -- extra packages for enterprise linux
# RUN yum install -y \
# 	https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
# RUN yum install -y \
# 	openslide-devel 

# # non-standard stuff we build from source goes here
# # ENV VIPSHOME /usr/local/vips
# ENV VIPSHOME /libvips
# ENV PKG_CONFIG_PATH $VIPSHOME/lib/pkgconfig

# ARG WEBP_VERSION=1.1.0
# ARG WEBP_URL=https://storage.googleapis.com/downloads.webmproject.org/releases/webp

# RUN cd /usr/local/src \
# 	&& wget ${WEBP_URL}/libwebp-${WEBP_VERSION}.tar.gz \
# 	&& tar xzf libwebp-${WEBP_VERSION}.tar.gz \
# 	&& cd libwebp-${WEBP_VERSION} \
# 	&& ./configure --enable-libwebpmux --enable-libwebpdemux \
# 		--prefix=$VIPSHOME \
# 	&& make V=0 \
# 	&& make install

# ARG VIPS_VERSION=8.10.5
# ARG VIPS_URL=https://github.com/libvips/libvips/releases/download

# RUN cd /usr/local/src \
# 	&& wget ${VIPS_URL}/v${VIPS_VERSION}/vips-${VIPS_VERSION}.tar.gz \
# 	&& tar xzf vips-${VIPS_VERSION}.tar.gz \
# 	&& cd vips-${VIPS_VERSION} \
# 	&& ./configure --prefix=$VIPSHOME \
# 	&& make V=0 \
# 	&& make install

# COPY requirements.txt /tmp
# COPY lambda_function.py lambda_function_original.py .
# RUN yum install python3 zip -y && \
#     pip3 install -r /tmp/requirements.txt --target ./package && \
#     cd package && rm -r *.dist-info __pycache__ && zip -r9 ../lambda.zip . && \
#     cd .. && zip -r9 lambda.zip $VIPSHOME/ lambda_function_original.py lambda_function.py


FROM public.ecr.aws/lambda/python:3.9

ENV WORK_DIR /working
WORKDIR $WORK_DIR

RUN yum update -y && \
    yum groupinstall "Development Tools" -y && \
    yum install wget tar gcc-c++ pkgconfig glib2 glib2-devel expat-devel -y

# libvips 및 의존성 설치
# RUN wget https://github.com/libvips/libvips/releases/download/v8.14.3/vips-8.14.3.tar.xz && \
#     tar Jxvf vips-8.14.3.tar.xz && \
#     cd vips-8.14.3 && \
#     meson setup build --prefix /libvips && \
#     cd build && \
#     meson compile && \
#     meson test && \
#     meson install
RUN wget https://github.com/libvips/libvips/releases/download/v8.10.5/vips-8.10.5.tar.gz && \
    tar zxvf vips-8.10.5.tar.gz && \
    cd vips-8.10.5 && \
    ./configure --prefix=$WORK_DIR/libvips && \
    make && \
    make install

COPY requirements.txt $WORK_DIR
COPY lambda_function.py $WORK_DIR
RUN yum install python3 zip -y && \
    pip3 install -r $WORK_DIR/requirements.txt --target $WORK_DIR/package && \
    cd $WORK_DIR/package && rm -r *.dist-info __pycache__ && zip -r9 /lambda.zip . && \
    cd $WORK_DIR/libvips && zip -r9 /lambda.zip . && \
    cd $WORK_DIR && zip -r9 /lambda.zip $WORK_DIR/lambda_function.py
# RUN zip -r9 lambda.zip lambda_function.py && \
#     yum install python3 zip -y && \
#     pip3 install -r /tmp/requirements.txt --target ./package && \
#     cd package && rm -r *.dist-info __pycache__ && zip -r9 ../lambda.zip . && \
#     cd /libvips && zip -r9 /lambda.zip .
# RUN yum install python3 zip -y && \
#     pip3 install -r /tmp/requirements.txt --target ./package && \
#     cd package && rm -r *.dist-info __pycache__ && zip -r9 ../lambda.zip . && \
#     echo "HERE" && ls && cd ../libvips && zip -r9 ../lambda.zip . && \
#     cd .. && zip -r9 lambda.zip lambda_function.py
#     # cd .. && zip -r9 lambda.zip /libvips/ lambda_function_original.py lambda_function.py
CMD [ "app.lambda_handler" ]
