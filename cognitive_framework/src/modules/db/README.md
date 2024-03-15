# db-pipeline

## Description
This is the db-pipeline that contains the functionality of generating the graph on Neo4J using the collected database. 
This pipeline is structured into three main files, each serving a distinct purpose in the context of generating a graph in Neo4J using data from a CSV file.  

**graph_builder.py** :  it contains the main function to generate the graph in Neo4J by reading data samples. Here, you generate nodes, relationships with the help of the defined types of nodes and relationships in api_utils.py.  
**api_utils.py** :  it contains the API functions that helps to create nodes and relathionships for the graph based on the defined types.    
**general_utils.py** :  it contains the general function that create nodes and relationshps in neo4j using py2neo library. Also, it has the function to read and extract the information from dataset file(.csv)  
**query.py** :  it contain the Cypher query that is possibly useful to understand our graph database.   
    
Please follow the in detail logs inside of each script...........  

## Getting started

To start using this repository, there are pre-requisite to setup. Here are the steps that you can follow.
1. Install Neo4J desktop on your local computer. [Neo4J Desktop installation](https://neo4j.com/download/?utm_source=google&utm_medium=PaidSearch&utm_campaign=GDB&utm_content=EMEA-X-Conversion-GDB-Text&utm_term=neo4j%20desktop%20install&gad_source=1&gclid=CjwKCAiAsIGrBhAAEiwAEzMlC2WFhsJvKKKDUvl-SKkL1ONS84M1p824G0HqjEYUDPEUu4KEWwOU-BoCykwQAvD_BwE)

2. Create a new project , then create a local DBMS to connect with this repository to generate the graph.
3. give the password for your generated local DBMS into the place in main.py (please follow the log file of the script)
4. start your local DBMS before you start run this code.

## Requirements

Required libraries.

```
py2neo
datetime
enum
csv
```

## Add your files

The dataset that you want to apply, need to be placed under the folder name of 'data'  
Note: this pipeline accept only once dataset file (.csv) to read and extract information for generating the graph.

## Installation

To start working with graph generation using this repository, you need to install it first.

```
git clone git@gitlab.com:idmg/glc/db.git
```

## Usage

Once you generate the graph, with the help of this repository using Neo4J, you can check the generated graph on your local DBMS neo4J Browser, or Neo4J Bloom  
Followings are some useful query to use on Neo4J Browser to visualize entire graph and delete entire graph  

1. Print entire graph in Neo4J Browser
```
MATCH (n)-[r]->(m) RETURN n, r, m

```
2. Delete all the nodes and relationships  
```
MATCH (n)
DETACH DELETE n
```

- Structure of the graph that this code generating :  

![](./figures/graph_architecture.png)

- The expected output in Neo4J Browser:  

![](./figures/output.png)
