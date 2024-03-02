from model.hbnn import HBNN 
from model.autoarima import AutoARIMA
import numpy as np


if __name__ == "__main__":
   
    # From KG
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
    #ts_from_kg = data_utils.get_timeseries(query) 

    datasets = [
        np.arange(1,1000,2),
#        np.random.randint(5, size=11),
#        pm.datasets.load_wineind(),
#        ts_from_kg
    ]
    for dataset in datasets:
        print(f'dataset: {dataset}')
       
        AutoARIMA(dataset, evaluate=10)
 
        HBNN(dataset, evaluate=10)
