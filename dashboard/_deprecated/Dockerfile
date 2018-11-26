#### Base OS ####
FROM phusion/baseimage:0.10.0

#### Build ####
ENV DEBIAN_FRONTEND noninteractive

#### Install Yarn ####
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list

RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -

RUN apt-get -y update
RUN apt-get -y install net-tools wget nano
RUN apt-get -y install yarn
RUN apt-get -y install nodejs

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

#### UI Setup ####
# To generate base files run: npx create-react-app app;create-react-app app
COPY app/ /zeta-ui/

#### Files ####
COPY scripts/run.sh /
RUN chmod +x /run.sh

#### Networking ####
EXPOSE 3000
EXPOSE 5000

#### Start ####
CMD ["/bin/bash", "/run.sh"]
