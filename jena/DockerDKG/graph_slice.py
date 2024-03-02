from rdflib import Graph

def print_graph_data(g):
    for s, p, o in g:
        print(f"Subject: {s}\nPredicate: {p}\nObject: {o}\n")

def slice_rdf_by_vin(input_file_path):
    g = Graph()
    g.parse(input_file_path, format='xml')

    # print_graph_data(g) # If you want to see the graph data

    vehicles = set()
    for vehicle_uri in g.subjects(predicate=None, object=None):
        if "Vehicle:" in str(vehicle_uri):
            vin = str(vehicle_uri).split(":")[-1]
            vehicles.add(vin)

    for i, vin in enumerate(vehicles):
        vehicle_graph = Graph()
        query = f"""
            CONSTRUCT {{
                ?s ?p ?o .
            }}
            WHERE {{
                ?s ?p ?o .
                FILTER (STRSTARTS(STR(?s), "urn:ngsi-ld:Vehicle:{vin}"))
            }}
        """
        results = g.query(query)
        for stmt in results:
            print(stmt)
            vehicle_graph.add(stmt)

        if len(vehicle_graph) > 0:
            print(f"Successfully extracted data for Vehicle: {vin}")
            namespaces_dict = dict(g.namespace_manager.namespaces())
            for prefix, namespace in namespaces_dict.items():
                vehicle_graph.bind(prefix, namespace)

            output_file_path = f"./Data/slice{i+1}.rdf"
            with open(output_file_path, "wb") as output_file:
                vehicle_graph.serialize(output_file, format='xml')
        else:
            print(f"Failed to extract data for Vehicle: {vin}")

if __name__ == "__main__":
    rdf_file_path = "./Data/data.rdf"
    slice_rdf_by_vin(rdf_file_path)
