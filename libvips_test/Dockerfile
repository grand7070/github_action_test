FROM amazonlinux:2

RUN yum update -y && \
    yum groupinstall "Development Tools" -y && \
    yum install wget tar gcc-c++ pkgconfig glib2 glib2-devel expat-devel -y

# libvips 및 의존성 설치
# RUN wget https://github.com/libvips/libvips/releases/download/v8.14.3/vips-8.14.3.tar.xz && \
#     tar Jxvf vips-8.14.3.tar.xz && \
#     cd vips-8.14.3 && ls && \
#     meson setup build --prefix /libvips && ls && \
#     cd build && ls && \
#     meson compile && \
#     meson test && \
#     meson install && ls
RUN wget https://github.com/libvips/libvips/releases/download/v8.10.5/vips-8.10.5.tar.gz && \
    tar zxvf vips-8.10.5.tar.gz && \
    cd vips-8.10.5 && \
    #./configure --prefix=/var/task/libvips && \
    ./configure --prefix=/libvips && \
    make && \
    make install
    # && echo "First!" && ls && echo "Second!" && ls /var/task/libvips

COPY requirements.txt /tmp
COPY lambda_function.py lambda_function_original.py .
RUN yum install python3 zip -y && \
    pip3 install -r /tmp/requirements.txt --target ./package && \
    cd package && rm -r *.dist-info __pycache__ && \
    # && echo "Fourth!" && ls && \
    zip -r9 ../lambda.zip . && \
    cd ../libvips && zip -r9 ../lambda.zip . && \
    cd .. && zip -r9 ../lambda.zip lambda_function_original.py lambda_function.py
    # && \
    # cd .. && echo "Fifth!" && ls && zip lambda.zip /var/task/libvips/ lambda_function_original.py lambda_function.py
