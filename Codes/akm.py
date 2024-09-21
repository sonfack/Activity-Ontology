from rdflib import Namespace, Graph, URIRef
from rdflib.namespace import RDF, OWL, RDFS


g_time = Graph()
g_time.parse("../time.owl")
g_core = Graph()
g_core.parse("../core_activity_ontology.ttl")
g_teaching = Graph()
g_teaching.parse("../teaching_akg.ttl")
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


def ontology_taxonomy(akg: Graph, core: Graph, time: Graph) -> None:
    """
    This function generates the taxonomy of a given activity knowledge graph.
    - akg: the activity knowledge graph 
    - core: the core activity ontology
    - time: the time ontology
    Example: ontology_taxonomy(g_teaching, g_core, g_time)
    """
    q_1 = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

            CONSTRUCT
            WHERE { ?class rdf:type owl:Class.
                          ?class ?predicate ?object .
            }"""
    q_2 = """
           PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
           PREFIX owl: <http://www.w3.org/2002/07/owl#>
           PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
           PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

           CONSTRUCT
           WHERE {
               ?class rdf:type owl:Class .
               ?subclass rdfs:subClassOf ?class
              }
          """
    akg_class = akg.query(q_1)
    print(len(akg_class))
    akg_class.serialize(destination="g_akg_class.ttl", format="turtle")
    g_akg_class = Graph()
    g_akg_class.parse("g_akg_class.ttl")
    akg_class_subclass = akg.query(q_2)
    print(len(akg_class_subclass))
    akg_class_subclass.serialize(destination="g_akg_class_subclass.ttl", format="turtle")
    g_akg_class_subclass = Graph()
    g_akg_class_subclass.parse("g_akg_class_subclass.ttl")
    core_class = core.query(q_1)
    print(len(core_class))
    resp = Graph()
    resp = g_core + g_time + g_akg_class_subclass + g_akg_class
    resp.serialize(destination="taxonomy.ttl", format="turtle")


ontology_taxonomy(g_teaching, g_core, g_time)
