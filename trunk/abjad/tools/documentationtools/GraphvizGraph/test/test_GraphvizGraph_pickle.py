import pickle
from abjad import *

def test_GraphvizGraph_pickle_01():

    graph = documentationtools.GraphvizGraph()
    graph.append(documentationtools.GraphvizSubgraph())
    graph[0].append(documentationtools.GraphvizNode())
    graph[0].append(documentationtools.GraphvizNode())
    graph[0].append(documentationtools.GraphvizNode())
    graph[0].append(documentationtools.GraphvizSubgraph())
    graph[0][-1].append(documentationtools.GraphvizNode())
    graph.append(documentationtools.GraphvizNode())
    edge = documentationtools.GraphvizEdge()(graph[0][1], graph[1])
    edge = documentationtools.GraphvizEdge()(graph[0][0], graph[0][-1][0])

    r'''
    digraph Graph {
        subgraph cluster_0 {
            node_0_0;
            node_0_1;
            node_0_2;
            subgraph cluster_0_3 {
                node_0_3_0;
            }
            node_0_0 -> node_0_3_0;
        }
        node_1;
        node_0_1 -> node_1;
    }
    '''

    pickled = pickle.loads(pickle.dumps(graph))

    assert graph.graphviz_format == pickled.graphviz_format
