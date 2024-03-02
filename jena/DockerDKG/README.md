# This repository contains the code for Docker Compose Stack for Fuseki

## Requirements
Docker needs to be installed to the system before running this code.

https://www.docker.com/

To install the required *Python* package(s), run the following command:
```bash
pip install -r requirements.txt
```

To work on a larger dataset, the [BTC-2019 Dataset](https://doi.org/10.1007/978-3-030-30796-7_11) can be downloaded by running the ```download.sh``` script inside the ```Data_btc-2019``` folder.

## Building the Docker Image & Composing the Stack
The docker code is modified from https://github.com/stain/jena-docker. You can take a look at the original code for more information.

------

Make sure to have the slices (like ```slice1.rdf```, ```slice2.rdf``` etc.) in the ```Data``` directory. You can run the ```graph_slice.py``` file to generate the slices:
```bash
python3 graph_slice.py
```

Build and compose the stack with
```bash
docker compose up
```
**Username** is ```admin``` and **password** is ```swarm```. The password is set in the ```shiro.ini``` file ```(Line 30)```.

Fuseki instances will be available at ```http://localhost:3030``` to ```http://localhost:3033```.

If you need to add more instances, just add them to the docker-compose.yml file and run the compose command again.

## Adding Data to Fuseki
By default, the four slices in the Data folder are pushed into the instances.

If you want to create more Jena Fuseki instances, just add more in the ```docker-compose.yml``` file and specify the **location** of the data file (for now supports ```rdf``` or ```nq```, both can be *gzipped*) *without extensions*, and the **extensions** separately.

If you need to change the data type, update the header format in the ```docker-entrypoint.sh (Line 74)```, the value of the ```CONTENT_TYPE```.
Use the following:
```bash
n3: text/n3; charset=utf-8
nt: text/plain
rdf: application/rdf+xml
owl: application/rdf+xml
nq: application/n-quads
trig: application/trig
jsonld: application/ld+json
```

# Python - Communication with Fuseki

FusekiCommunicator can be found [here](https://github.com/glaciation-heu/IceStream/tree/development/metadata_service).

It uses the ```SPARQLWrapper``` library to communicate with Fuseki. You can find the detailed documentation [here](https://sparqlwrapper.readthedocs.io/en/latest/#).

For now, it only supports ```SELECT``` queries.

Calling other queries is possible, like adding data, etc. It might require minor changes to the code

# Python - Graph Slicing
```graph_slice.py``` includes a very straightforward slicing code. 

This was written to slice the MOSAICrOWN data we got from Dell EMC. It contains data coming from different vehicles.

The code slices the graph based on the ```vehicle``` property. It generates a new graph for each vehicle and saves it in the ```Data``` folder.