FROM ubuntu:bionic
RUN apt-get update -y
RUN apt-get install software-properties-common -y
RUN apt-get install python3.6 python3-pip virtualenv git unzip -y
RUN pip3 --version; pip3 install --upgrade pip
RUN mkdir /opt/purestorage_restapi/
COPY ./ /opt/purestorage_restapi/
RUN pip install /opt/purestorage_restapi/.

