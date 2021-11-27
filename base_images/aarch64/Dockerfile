FROM nvcr.io/nvidia/l4t-base:r32.6.1

RUN apt-get update
RUN apt-get install -y python3-pip cmake libpng-dev libopenblas-dev liblapack-dev libjpeg-dev
RUN pip3 install --upgrade pip

RUN pip3 install face_recognition
ENV OPENBLAS_CORETYPE=ARMV8
