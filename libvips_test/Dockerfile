FROM amazonlinux:2

RUN yum update -y && \
    yum groupinstall "Development Tools" -y && \
    yum install wget tar gcc-c++ pkgconfig glib2 glib2-devel -y

# libvips 및 의존성 설치
RUN wget https://github.com/libvips/libvips/releases/download/v8.10.5/vips-8.10.5.tar.gz && \
    tar zxvf vips-8.10.5.tar.gz && \
    cd vips-8.10.5 && \
    ./configure --prefix=/var/task/libvips && \
    make && \
    make install

COPY requirements.txt /tmp
RUN yum install python3 zip -y && \
    pip3 install -r /tmp/requirements.txt --target ./package && \
    zip -r9 /var/task/libvips/ /package/
