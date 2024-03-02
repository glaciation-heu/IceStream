#!/bin/bash
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

set -e

if [ ! -f "$FUSEKI_BASE/shiro.ini" ] ; then
  # First time
  echo "###################################"
  echo "Initializing Apache Jena Fuseki"
  cp "$FUSEKI_HOME/shiro.ini" "$FUSEKI_BASE/shiro.ini"
  echo "###################################"
fi

if [ -d "/fuseki-extra" ] && [ ! -d "$FUSEKI_BASE/extra" ] ; then
  ln -s "/fuseki-extra" "$FUSEKI_BASE/extra"
fi

# fork
exec "$@" &

TDB_VERSION=''
if [ ! -z ${TDB+x} ] && [ "${TDB}" = "2" ] ; then
  TDB_VERSION='tdb2'
else
  TDB_VERSION='tdb'
fi

# Wait until server is up
echo "Waiting for Fuseki to finish starting up..."
until $(curl --output /dev/null --silent --head --fail http://localhost:3030); do
  sleep 1s
done

CONTENT_TYPE="application/rdf+xml"
# If slice is compressed, decompress
FILE="`echo /staging/slice*`"
DELETE_AFTER_DONE=0
if [ "${FILE: -3}" == ".gz" ]
then
  echo "Decompressing the data file"
  gzip -dc $FILE > decompressed_slice

  if [ "${FILE: -6}" == ".nq.gz" ]
  then
    CONTENT_TYPE="application/n-quads"
  fi

  FILE="decompressed_slice"
  DELETE_AFTER_DONE=1
elif [ "${FILE: -3}" == ".nq" ]
then
  CONTENT_TYPE="application/n-quads"
fi

# Add datasets
echo "#############################"
echo "Adding datasets"
curl -X POST "http://localhost:3030/$/datasets" -u "admin:swarm" -d "dbName=slice&dbType=${TDB_VERSION}"


# Load the content into the dataset
echo "Loading content into the dataset"

if [ "$CONTENT_TYPE" == "application/n-quads" ]
then
  # To make sure there is no heap problem while loading big datafiles, limit the number of lines loaded at a time
  MAX_LINE_NUM=15000
  N_nquads=`wc -l $FILE | cut -d' ' -f1`
  i=1
  while [ $i -le $N_nquads ]
  do
    awk -v n1=$i -v n2="`expr $i + $MAX_LINE_NUM`" 'NR >= n1 && NR < n2' $FILE > "slice"
    i=`expr $i + $MAX_LINE_NUM`

    curl -X POST "http://localhost:3030/slice/data" -u "admin:swarm" -H "Content-Type: $CONTENT_TYPE" -T "slice"
  done
  rm -f "slice"
else
  curl -X POST "http://localhost:3030/slice/data" -u "admin:swarm" -H "Content-Type: $CONTENT_TYPE" -T "$FILE"
fi

if [ $DELETE_AFTER_DONE -eq 1 ]
then
  rm -f $FILE
fi

echo "--- Fuseki Instance is Available ---"
unset ADMIN_PASSWORD # Don't keep it in memory

# rejoin our exec
wait