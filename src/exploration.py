import kglab
from rdflib import Graph
from rdflib.namespace import RDF, OWL
# Visualization
import io
import pydotplus
from IPython.display import display, Image
from rdflib.tools.rdf2dot import rdf2dot

kg = kglab.KnowledgeGraph()
kg.load_rdf("./pkmoontologySchool.ttl", format="ttl")


measure = kglab.Measure()
measure.measure_graph(kg)

print("edges: {}\n".format(measure.get_edge_count()))
print("nodes: {}\n".format(measure.get_node_count()))


def visualize(graph):
    stream = io.StringIO()
    rdf2dot(graph, stream, opts={display})
    dg = pydotplus.graph_from_dot_data(stream.getvalue())
    png = dg.create_png()
    png.write_png("graph_img.png")
    display(Image(png))


g = Graph()
g.parse("./pkmoontologySchool.ttl")

visualize(g)

for myclasses in g.subjects(RDF.type, OWL.Class):
    print(myclasses)
