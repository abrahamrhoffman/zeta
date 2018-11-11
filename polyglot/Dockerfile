FROM oracle/graalvm-ce:1.0.0-rc8

#### AUTHOR ####
MAINTAINER Abe Hoffman "abhoffman@paypal.com"

#### Additional Language Support ####
# C, C++, Java, JavaScript and non-native Python included
RUN gu install ruby && \
    gu install r

#### Dependencies ####
RUN yum -y install python-pip && \
    yum -y install python-devel

RUN pip install ujson && \
    pip install cython && \
    pip install --no-binary :all: falcon

#### Copy code to working directory ####
RUN mkdir /x
COPY src /x/src

#### Expose the external port for the API ####
EXPOSE 8444

#### Start the Service ####
CMD ["/bin/bash", "/x/src/scripts/run.sh"]
