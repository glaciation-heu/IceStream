#   Licensed to the Apache Software Foundation (ASF) under one or more
#   contributor license agreements.  See the NOTICE file distributed with
#   this work for additional information regarding copyright ownership.
#   The ASF licenses this file to You under the Apache License, Version 2.0
#   (the "License"); you may not use this file except in compliance with
#   the License.  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# Use a base image
FROM eclipse-temurin:17-jre-alpine

ENV LANG C.UTF-8
RUN set -eux; \
    apk -U upgrade; \
    apk add bash curl ca-certificates findutils coreutils gettext pwgen procps tini; \
    rm -rf /var/cache/apk/*

# Download Fuseki
ENV FUSEKI_SHA512 84079078b761e31658c96797e788137205fc93091ab5ae511ba80bdbec3611f4386280e6a0dc378b80830f4e5ec3188643e2ce5e1dd35edfd46fa347da4dbe17
ENV FUSEKI_VERSION 4.9.0
ENV ASF_MIRROR https://www.apache.org/dyn/mirrors/mirrors.cgi?action=download&filename=
ENV ASF_ARCHIVE https://archive.apache.org/dist/

# Config and data
ENV FUSEKI_BASE /fuseki

# Installation folder
ENV FUSEKI_HOME /jena-fuseki

WORKDIR /tmp
# published sha512 checksum
RUN echo "$FUSEKI_SHA512  fuseki.tar.gz" > fuseki.tar.gz.sha512
# Download/check/unpack/move in one go (to reduce image size)
RUN     (curl --location --silent --show-error --fail --retry-connrefused --retry 3 --output fuseki.tar.gz ${ASF_MIRROR}jena/binaries/apache-jena-fuseki-$FUSEKI_VERSION.tar.gz || \
    curl --fail --silent --show-error --retry-connrefused --retry 3 --output fuseki.tar.gz $ASF_ARCHIVE/jena/binaries/apache-jena-fuseki-$FUSEKI_VERSION.tar.gz) && \
    sha512sum -c fuseki.tar.gz.sha512 && \
    tar zxf fuseki.tar.gz && \
    mv apache-jena-fuseki* $FUSEKI_HOME && \
    rm fuseki.tar.gz* && \
    cd $FUSEKI_HOME && rm -rf fuseki.war && chmod 755 fuseki-server

# Test the install by testing it's ping resource. 20s sleep because Docker Hub.
RUN  $FUSEKI_HOME/fuseki-server & \
    sleep 20 && \
    curl -sS --fail 'http://localhost:3030/$/ping'

# No need to kill Fuseki as our shell will exit after curl

# As "localhost" is often inaccessible within Docker container,
# we'll enable basic-auth with a random admin password
# (which we'll generate on start-up)
COPY shiro.ini $FUSEKI_HOME/shiro.ini
COPY docker-entrypoint.sh /
RUN chmod 755 /docker-entrypoint.sh


COPY load.sh $FUSEKI_HOME/
COPY tdbloader $FUSEKI_HOME/
COPY tdbloader2 $FUSEKI_HOME/
RUN chmod 755 $FUSEKI_HOME/load.sh $FUSEKI_HOME/tdbloader $FUSEKI_HOME/tdbloader2
#VOLUME /staging

# Create a fuseki user and group
RUN addgroup -S fuseki && \
    adduser -G fuseki -S -D -H fuseki

# Where we start our server from
WORKDIR $FUSEKI_HOME
RUN chown -R fuseki:fuseki $FUSEKI_HOME

# Make sure we start with empty /fuseki
RUN mkdir -p $FUSEKI_BASE; \
    rm -rf $FUSEKI_BASE/*; \
    chown -R fuseki:fuseki $FUSEKI_BASE
VOLUME $FUSEKI_BASE

# Accept arguments for the LOCATION and EXTENSION (defaults if not provided)
ARG LOCATION="./Data/slice1"
ARG EXTENSION=".rdf"

# Copy the corresponding RDF file based on the slice number
COPY ${LOCATION}${EXTENSION} /staging/slice${EXTENSION}

EXPOSE 3030
USER fuseki

ENTRYPOINT ["/sbin/tini", "--", "sh", "/docker-entrypoint.sh"]
CMD ["/jena-fuseki/fuseki-server"]
