from rdflib import Namespace, Graph, URIRef
from rdflib.namespace import RDF, OWL, RDFS
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random
 
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
    activities_list = [str(activity) if as_str else activity for activity in akg.subjects(
        predicate=RDF.type,                                                  object=cao_namespace.Activity, unique=True)]
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
    akg_class_subclass.serialize(
        destination="g_akg_class_subclass.ttl", format="turtle")
    g_akg_class_subclass = Graph()
    g_akg_class_subclass.parse("g_akg_class_subclass.ttl")
    core_class = core.query(q_1)
    print(len(core_class))
    resp = Graph()
    resp = g_core + g_time + g_akg_class_subclass + g_akg_class
    resp.serialize(destination="taxonomy.ttl", format="turtle")


def visualize_akg():
    g = g_teaching+g_core+g_time
    G = rdflib_to_networkx_multidigraph(g)

    # Plot Networkx instance of RDF Graph
    pos = nx.spring_layout(G, scale=2)
    edge_labels = nx.get_edge_attributes(G, 'r')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw(G, with_labels=True)

    # if not in interactive mode for
    plt.show()


def random_color_generator():
    color = random.choice(list(mcolors.CSS4_COLORS.keys()))
    return color

def simple_akg():
    simple_graph = nx.Graph()
    akg =  g_teaching+g_core+g_time
    ac_query = """
                 PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX tao: <http://sonfack.com/2023/12/tao/>
PREFIX cao: <http://sonfack.com/2023/12/cao/>
SELECT ?label
WHERE {
	
	?activity rdf:type cao:Activity ; rdfs:label ?label .

}
               """
    query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX tao: <http://sonfack.com/2023/12/tao/>
            PREFIX cao: <http://sonfack.com/2023/12/cao/>

            SELECT ?label1 ?p  ?o ?label2
            WHERE { 
	          {
		     ?o ?p ?s1.
		     ?o ?p ?s2  .
		     ?s1 a cao:Activity .
                     ?s1 rdfs:label ?label1 .
		     ?s2 a cao:Activity .
                     ?s2 rdfs:label ?label2 .
		    FILTER ((?p != rdf:type ) && (?s1 != ?s2))
	          }UNION{ 
	
		    ?s1 ?p ?o .
		    ?s2 ?p ?o .
		    ?s1 a cao:Activity .
                    ?s1 rdfs:label ?label1 .
		    ?s2 a cao:Activity .
                    ?s2 rdfs:label ?label2 .
		   FILTER ((?p != rdf:type ) && (?s1 != ?s2))
	
	         }
          }
       """
    list_edges = []
    simple_result = akg.query(query)
    for quad in simple_result:
        list_edges.append((str(quad[0]), str(quad[-1])))
    print(list_edges)
    isolate = []
    activity_result = akg.query(ac_query)
    simple_graph.add_edges_from(list_edges)
    for act in activity_result:
        if str(act[0]) not in simple_graph.nodes():
            simple_graph.add_node(str(act[0]))
            isolate.append({str(act[0])})
    nx.draw(simple_graph, with_labels=True)
    plt.show()
    list_color = []
    communities = nx.community.louvain_communities(simple_graph, seed=900000)
    print("+++++", communities)
    community_graph = nx.Graph()
    community_graph = simple_graph
    nodes_color = []
    for community in communities:
        color = random_color_generator()
        list_color.append(color)
        for node in community_graph.nodes():
            if node in list(community):
                nodes_color.append(color)
    nx.draw(community_graph, with_labels=True, node_color=nodes_color)
    plt.show()
    return communities, list_color



def rdf_instance_graph():
    akgin = g_teaching+g_core+g_time
    queryin = """
           
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX tao: <http://sonfack.com/2023/12/tao/>
PREFIX cao: <http://sonfack.com/2023/12/cao/>
SELECT DISTINCT ?s ?sname ?pro  ?obj ?oname
WHERE {
	{
	SELECT ?s ?slabel
	WHERE { 
		?s rdf:type ?o .
		?o rdf:type owl:Class .
		OPTIONAL {
			?s rdfs:label ?slabel .
		}
			
 		}
	}
	?s ?pro ?obj .
	OPTIONAL {
	?obj rdfs:label ?olabel .}
	bind( IF (BOUND(?slabel), ?slabel,  "_") as ?sname)
                  bind( IF (BOUND(?olabel), ?olabel,  "_") as ?oname)
	FILTER  isIRI(?obj)
	FILTER (?obj  != owl:NamedIndividual && ?pro != rdf:type)
}ORDER BY ?s            """
    result = akgin.query(queryin)

    list_edges  = []
    for elements in result:
        print("###", elements)
        node1 = str(elements[1])
        node2 = str(elements[4])
        
        if str(elements[1]) == "_" and len(str(elements[1])) ==1 :
            if "/" in str(elements[0]):
                node = str(elements[0]).split("/")[-1].split("-")
                node1 = node[0]+"-"+node[1]+"-"+node[2]
            else:
                node = str(elements[0]).split("-")
                node1 = node[0]+"-"+node[1]+"-"+node[2]
        if str(elements[4]) == "_" and len(str(elements[4]))==1:
            if "/" in str(elements[3]):
                node = str(elements[3]).split("/")[-1].split("-")
                node2 = node[0]+"-"+node[1]+"-"+node[2]
            else:
                node = str(elements[3]).split("-")
                node2 = node[0]+"-"+node[1]+"-"+node[2]
        print(node1, "-", node2)

        list_edges.append((node1, node2))
    instances_graph = nx.Graph()
    instances_graph.add_edges_from(list_edges)
    pos = nx.spring_layout(instances_graph, seed=3113794652)
    nx.draw(instances_graph,  edge_color='black',  with_labels=True)
    plt.show()



def akg_community_graph(colors, communities):
    akgin = g_teaching+g_core+g_time
    queryin = """
           
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX tao: <http://sonfack.com/2023/12/tao/>
PREFIX cao: <http://sonfack.com/2023/12/cao/>
SELECT DISTINCT ?s ?sname ?pro  ?obj ?oname
WHERE {
	{
	SELECT ?s ?slabel
	WHERE { 
		?s rdf:type ?o .
		?o rdf:type owl:Class .
		OPTIONAL {
			?s rdfs:label ?slabel .
		}
			
 		}
	}
	?s ?pro ?obj .
	OPTIONAL {
	?obj rdfs:label ?olabel .}
	bind( IF (BOUND(?slabel), ?slabel,  "_") as ?sname)
                  bind( IF (BOUND(?olabel), ?olabel,  "_") as ?oname)
	FILTER  isIRI(?obj)
	FILTER (?obj  != owl:NamedIndividual && ?pro != rdf:type)
}ORDER BY ?s            """
    result = akgin.query(queryin)

    list_edges  = []
    for elements in result:
        print("###", elements)
        node1 = str(elements[1])
        node2 = str(elements[4])
        
        if str(elements[1]) == "_" and len(str(elements[1])) ==1 :
            if "/" in str(elements[0]):
                node = str(elements[0]).split("/")[-1].split("-")
                node1 = node[0]+"-"+node[1]+"-"+node[2]
            else:
                node = str(elements[0]).split("-")
                node1 = node[0]+"-"+node[1]+"-"+node[2]
        if str(elements[4]) =="_" and len(str(elements[4]))==1:
            if "/" in str(elements[3]):
                node = str(elements[3]).split("/")[-1].split("-")
                node2 = node[0]+"-"+node[1]+"-"+node[2]
            else:
                node = str(elements[3]).split("-")
                node2 = node[0]+"-"+node[1]+"-"+node[2]
        print(node1, "-", node2)

        list_edges.append((node1, node2))
    akg_community_graph = nx.Graph()
    akg_community_graph.add_edges_from(list_edges)
    nx.draw(akg_community_graph, with_labels=True)
    plt.show()

    community_graph = nx.Graph()
    pos = nx.spring_layout(community_graph)
    
    nodes_color = []
    cnodes = []
    onodes = []
    for community in range(len(communities)):
        onodes = onodes + list(communities[community])
        cnodes.append(list(communities[community]))
        print("%%%%", cnodes)

    res_nodes =[]                    
    for node in akg_community_graph.nodes:
        if node not  in onodes:
            res_nodes.append(node)
    print("%%%%", res_nodes)
    cnodes.append(res_nodes)
    #community_graph.add_edges_from(list_edges)
    colors_n = []
    colors_n = colors_n+colors
    colors_n.append("white")
    print("%%%%", colors_n)
    for node in akg_community_graph.nodes():
        if node in cnodes[0]:
            nodes_color.append(colors_n[0])
        if node in cnodes[1]:
            nodes_color.append(colors_n[1])
        if node in cnodes[2]:
            nodes_color.append(colors_n[2])
        if node in cnodes[3]:
            nodes_color.append(colors_n[3])
    nx.draw(akg_community_graph, with_labels=True, node_color=nodes_color)
    plt.show()


def akg_map():
    instance_query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX tao: <http://sonfack.com/2023/12/tao/>
PREFIX cao: <http://sonfack.com/2023/12/cao/>
SELECT ?o  (COUNT(DISTINCT ?s) AS ?count)
WHERE {
	
		?s rdf:type ?o.
		?o rdf:type owl:Class.
	
 	

}group by ?o
    """
    map_g = nx.Graph()
    akg_g = g_teaching+g_core+g_time
    result  = akg_g.query(instance_query)
    node_sizes = []
    nodes = []
    for inst in result :
        node  = str(inst[0]).split("/")[-1]
        if "#" in node:
            node = node.split("#")[-1]
        nodes.append(node)
        node_sizes.append(300*int(str(inst[1])))
    print(node_sizes)
    map_g.add_nodes_from(nodes)
    map_g.add_edges_from([])
    pos = nx.spring_layout(map_g)
    #nx.draw(map_g, pos,  node_size = node_sizes,  with_labels=True) 
    #plt.show()

    for instx in result:
        for insty in result:
            x = instx[0]
            y = insty[0]
            template_query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX tao: <http://sonfack.com/2023/12/tao/>
            PREFIX cao: <http://sonfack.com/2023/12/cao/>
            SELECT ?p
            WHERE {
            {
            ?insx rdf:type  <"""+x+"""> .
            ?insy rdf:type <"""+y+"""> .  
            }
            { ?insx ?p ?insy .
            }UNION{
            ?insy ?p ?insx .
            }

            }
            """
            print("*********", template_query)
            if x != y:
                new_result  = akg_g.query(template_query)
                for edge in new_result:
                    node1  = str(x.split("/")[-1])
                    if "#" in node1 :
                        node1 = node1.split("#")[-1]
                    node2  = str(y.split("/")[-1])
                    if "#" in node2 :
                        node2 = node2.split("#")[-1]
                    map_g.add_edge(node1, node2, label=edge[0].split("/")[-1])
    edge_labels = dict([((n1, n2), d['label']) for n1, n2, d in map_g.edges(data=True)])
   
    nx.draw_networkx_edge_labels(map_g, pos)
    # nx.draw_random(map_g, node_size = node_sizes,  with_labels=True) 
    plt.show()


# ontology_taxonomy(g_teaching, g_core, g_time)
# visualize_akg("../teaching_akg.ttl")
# visualize_akg()
### communities, colors = simple_akg()
### akg_community_graph(colors, communities)
# rdf_instance_graph()
akg_map()
