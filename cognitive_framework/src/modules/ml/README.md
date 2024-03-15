# GLACIATION/AI/ML modules


## Description
This project aims to develop a Machine Learning model for energy efficient scheduling of tasks in Kubernetes platform. It applies a Graph Neural Network(GNN) model on a graph for link prediction.

For more information about required tools and packages, take a look at the following links:

- [Neo4j](https://neo4j.com/) - Graph Database Management System
- [PyG](https://pyg.org/) - Python Graph Neural Networks Library
- [fastRP](https://neo4j.com/docs/graph-data-science/current/machine-learning/node-embeddings/fastrp/?utm_source=google&utm_medium=PaidSearch&utm_campaign=GDB&utm_content=EMEA-X-Awareness-GDB-Text&utm_term=&gad_source=1&gclid=CjwKCAiAgeeqBhBAEiwAoDDhn2vMY_jcRPv9O64PFcYGtJ3VSAUI54S1nEuB3hnpBx_zXlA8b5TwEBoCxMsQAvD_BwE) Fast Random Projection
- [Metapath2Vec](https://ericdongyx.github.io/metapath2vec/m2v.html)
- [Node2Vec](http://dl.acm.org/citation.cfm?id=2939672.2939754)


## How to change configurations
In the follwoing table there is a list of configuration parameters and their explanations. these configurations can be changed in `config` script.
|Config|Description|
|:--|:------|
|`workload_query`| The Cypher query to read workload data from neo4j database|
|`worknode_query`| The Cypher query to read workerNode data from neo4j database|
|`allocation_query`|The Cypher query to read resource allocatd data from neo4j database|
|`num_val`| The ratio of validation data|
|`num_test`| The ratio of test data|
|`hidden_channels`| The number of hidden channels in the final neural network which is used for link prediction|
|`learning_rate`|The learning rate of final neural network which is used for link prediction|
|`train_epoch`| The number of epoch in training process|
|`top_k_predicts`| The number of proposed WorkerNode for each Workload|
|`node_ebedding_name`| The name of node embedding approach including fastrp,metapath2vec,node2vec,metapath2vec, and metapath2vec_context|
|`configuration for fastRP`| The configuration of fastRP node embedding approach|
|`visualize`| It can be True of False.  If  true, a scatterplot of the  node embedding vectors is plotted.

