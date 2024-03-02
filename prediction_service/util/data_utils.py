import tensorflow as tf
import numpy as np
import pandas as pd

from pprint import pprint
from rdflib import Graph, BNode, Literal, Namespace
from rdflib.namespace import RDF, PROV, XSD
from SPARQLWrapper import SPARQLWrapper, JSON


def create_KG(city='DAYTON'):
    """ Create mock KG of energy consumption 
    Datasource: https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption/
    """
    data = pd.read_csv(
        f'data/{city}_hourly.csv',
        header=0,
        names=['Datetime', 'Energy Consumption'],
        parse_dates=['Datetime']
    )#[:1000]
    print(data)
    
    # Create Graph
    g = Graph()
    OM = Namespace('http://www.ontology-of-units-of-measure.org/resource/om-2/')
    g.bind('om', OM)
    # Iterate each row and populate graph
    for ind, r in data.iterrows():
        ts_time = r['Datetime']
        ts_val = r['Energy Consumption']
        # Create each timeseries data point
        ts = BNode()
        g.add((ts, RDF.type, PROV.Entity))
        ts_time = Literal(ts_time, datatype=XSD.dateTime)
        g.add((ts, PROV.generatedAtTime, ts_time))

        g.add((ts, RDF.type, OM.Measure))
        ts_val = Literal(ts_val, datatype=XSD.float) 
        g.add((ts, OM.hasNumericalValue, ts_val))
        g.add((ts, OM.hasUnit, OM.megawatt))
        
    g.serialize(destination=f'data/{city}.ttl')
    

def get_timeseries(sparql_query:str, loc='data/DAYTON.ttl'):
    """ Return timeseries as a sequence of numbers
    
    :param loc: file destination or endpoint address
    :param sparql_query: query to be executed
    """
    g = Graph()
    g.parse(loc)
    res = g.query(sparql_query)
    ts = [r.measure.toPython() for r in res]

    return ts


def window_dataset(series:np.array, window_size:int):
    """ Return window dataset with (X,y) format
        for DL-based time series models
    
    :param series: time series data
    :param window_size: window size - len(X)
    """
    dataset = tf.data.Dataset.from_tensor_slices(series)
    dataset = dataset.window(
        window_size+1,
        shift=1,
        drop_remainder=True
    )
    dataset = dataset.flat_map(
        lambda x: x.batch(window_size+1)
    )
    dataset = dataset.map(lambda x: (x[:-1], x[-1:]))
    data, labels = [], []
    for (x, y) in dataset.as_numpy_iterator():
        data.append(x)
        labels.append(y[0])
    data = np.array(data).astype(float)
    labels = np.array(labels).astype(float)
    return (data, labels)
    

if __name__ == '__main__':
    #create_KG()

    query = """
    prefix om: <http://www.ontology-of-units-of-measure.org/resource/om-2/>
    prefix prov: <http://www.w3.org/ns/prov#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT ?measure
    WHERE {
      ?subject rdf:type om:Measure .
      ?subject om:hasNumericalValue ?measure .
      ?subject prov:generatedAtTime ?date .
    }
    ORDER BY ASC(?date)
    """
    #get_timeseries(query) 
    #print(window_dataset(
    #    np.arange(1, 300, 2),
    #    window_size=3
    #))


    # Fuseki test
    sparql = SPARQLWrapper(
        endpoint='http://localhost:3030/ds/update'
    )
    sparql.setReturnFormat(JSON)
    sparql.setQuery("""
        SELECT * WHERE {
            ?s ?p ?o
        }
        """
    )
    sparql.setQuery("""
        prefix log: <http://example.org/ont/transaction-log/> 
        prefix srv: <http://example.org/data/server/> 
        prefix txn: <http://example.org/data/transaction/> 
        prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
        
        INSERT DATA {
            txn:136  a               log:Transaction;
                log:processedAt  "2015-10-16T10:22:23"^^xsd:dateTime;
                log:processedBy  srv:A;
                log:statusCode   200 .
        }
        """
    )
    try:
        ret = sparql.queryAndConvert()
        print(ret)
        #for r in ret['results']['bindings']:
        #    print(r)
    except Exception as e:
        print(e)
