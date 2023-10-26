import pandas as pd

from pprint import pprint
from rdflib import Graph, BNode, Literal, Namespace
from rdflib.namespace import RDF, PROV, XSD


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


if __name__ == '__main__':
    create_KG()

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
    get_timeseries(query) 
