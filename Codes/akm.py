from rdflib import Namespace, Graph, URIRef
from rdflib.namespace import RDF, OWL, RDFS

akg_file = "../core_activity_ontology.ttl"
g = Graph()
g.parse(akg_file)
akg_namespace = Namespace("http://sonfack.com/2023/12/tao/")
cao_namespace = Namespace("http://sonfack.com/2023/12/cao/")


def read_all_activities(akg: Graph, as_str=True) -> list:
    """This function returns all activities of an activity knowledge graph
    - akg: an activity knowledge graph as parsed by RDFLib
    - as_str: (boolean) tells if the activities are simple str default = True

    Example:
    read_all_activities(g, False)
    """
    activities_list = [str(activity) if as_str else activity for activity in akg.subjects(predicate=RDF.type,                                                  object=cao_namespace.Activity, unique=True)]
    return activities_list


def read_akg_node(node_uri: str, akg: Graph, as_str=True) -> dict:
    """This function returns all elements directly linked to a akg node
    - activity_uri (string): the given activity uri in graph akg
    - akg (Graph): an activity knowledge graph as parsed by RDFLib
    - as_str: if one want to have result as a dictionary of string.
              if False, result is a dictionary of URIRef

    Examples on how to use read_akg_node
    read_akg_node("pypractical-f18f0361-3f12-4b3d-9459-ce2a019b4668", g, False)
    read_akg_node("book-0626b11e-a0d8-4eab-9485-4d42a51e8581", g)

    """
    activity_info = {}
    activity_uri_ref = f"{akg_namespace}{node_uri}"
    print(activity_uri_ref)
    for act_predicate, act_object in akg.predicate_objects(subject=URIRef(activity_uri_ref)):
        pred = act_predicate
        obj = act_object
        if as_str:
            pred = str(act_predicate)
            obj = str(act_object)
        if pred in activity_info:
            existing_objects = activity_info[pred] + [obj]
            activity_info[pred] = existing_objects
        else:
            activity_info[pred] = [obj]
    return activity_info


def ontology_extraction(akg: Graph) -> None:
    onto_g = Graph()
    owl_class = f"<{OWL.Class}>"
    rdf_type = f"<{RDF.type}>"
    rdfs_subclass = f"<{RDFS.subClassOf}>"
    print(owl_class)
    q_1 = """CONSTRUCT
            WHERE { ?class """+rdf_type+""" """+owl_class+""".
                          ?class ?predicate ?object .
            }"""
    q_2 = """CONSTRUCT
            WHERE { ?class """+rdf_type+""" """+owl_class+""".
                    ?subclass """+rdfs_subclass+""" ?class.
                    ?subclass ?subpred ?subobj .   
                }"""
    resp_1 = g.query(q_1)
    print(len(resp_1))
    resp_1.serialize(destination="g_1.ttl", format="turtle")
    resp_2 = g.query(q_2)
    print(len(resp_2))
    resp_2.serialize(destination="g_2.ttl", format="turtle")

    
ontology_extraction(g)
