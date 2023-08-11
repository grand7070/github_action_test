FROM amazonlinux:2

RUN yum update -y && \
    yum groupinstall "Development Tools" -y && \
    yum install wget tar gcc-c++ pkgconfig glib2 glib2-devel expat-devel -y

# libvips 및 의존성 설치
RUN wget https://github.com/libvips/libvips/releases/download/v8.14.3/vips-8.14.3.tar.xz && \
    tar Jxvf vips-8.14.3.tar.xz && \
    cd vips-8.14.3 && \
    ./configure --prefix=/libvips && \
    make && \
    make install

COPY requirements.txt /tmp
COPY lambda_function.py .
RUN yum install python3 zip -y && \
    pip3 install -r /tmp/requirements.txt --target ./package && \
    cd package && rm -r *.dist-info __pycache__ && zip -r9 ../lambda.zip . && \
    cd .. && zip lambda.zip /libvips/ lambda_function_original.py lambda_function.py
