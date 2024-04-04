import json

from openapi_server.models.metric import Metric
from SPARQLWrapper import SPARQLWrapper, JSON


def query(metricID):
    sparql = SPARQLWrapper("http://192.168.0.94:3030/ds/sparql")
    sparql.setReturnFormat(JSON)
    
    # gets the first 3 geological ages
    # from a Geological Timescale database,
    # via a SPARQL endpoint

    query = """ 
    prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    prefix om: <http://www.ontology-of-units-of-measure.org/resource/om-2/>
    prefix prov: <http://www.w3.org/ns/prov#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT ?measure ?date
    WHERE {
      ?subject rdf:type om:Measure .
      ?subject om:hasNumericalValue ?measure .
      ?subject prov:generatedAtTime ?date .
    }
    ORDER BY ASC(?date)
    LIMIT 30
    """

    sparql.setQuery("""
        SELECT ?a
        WHERE {
            ?a <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?b .
        }
        LIMIT 3
        """
    )

    sparql.setQuery(query)
    
    try:
        # Using SPARQL results
        #ret = sparql.queryAndConvert()
        #metric = Metric(id=metricID, time=[], value=[])
        #for r in ret["results"]["bindings"]:
        #    metric.value.append(float(r['measure']['value']))
        #    metric.time.append(r['date']['value'])
        #print(metric) 
        #ts_dict = {
        #    'id': metricID,
        #    'time': metric.time,
        #    'value': metric.value
        #}

        # Dummpy data for testing
        ts_dict = {
            "aggregation_interval": 90,
            "forecasting_lower_bounds": [
              4
            ],
            "forecasting_model": "ARIMA",
            "forecasting_period": 1,
            "forecasting_upper_bounds": [
              6
            ],
            "forecasting_values": [
              5
            ],
            "metricId": metricID,
            "time": [
              "2024-03-20"
            ],
            "timeseries": [
              1,2,3,4
            ]
        }        

        ts_json = json.dumps(ts_dict)
        
        return ts_json
    except Exception as e:
        print(e)
        return str(e)


if __name__ == '__main__':
    print(query(0))
