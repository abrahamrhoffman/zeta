#### IMAGE ####
FROM phusion/baseimage:0.10.0

#### AUTHOR ####
MAINTAINER Abe Hoffman "abhoffman@paypal.com"

#### BUILD ####
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y python python-dev
RUN apt-get install -y net-tools
RUN apt-get install -y python-pip

RUN pip install --upgrade pip
RUN pip install dask distributed --upgrade
RUN pip install ujson cython
RUN pip install --no-binary :all: falcon

RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /root/.cache

RUN mkdir /x
COPY src /x/src

#### Networking ####
EXPOSE 8444
EXPOSE 8445

#### Start the Service ####
CMD ["/bin/bash", "/x/src/scripts/run.sh"]
