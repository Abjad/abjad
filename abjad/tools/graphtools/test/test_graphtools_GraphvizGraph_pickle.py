import abjad
import pickle


def test_graphtools_GraphvizGraph_pickle_01():
    graph = abjad.graphtools.GraphvizGraph()
    assert str(graph) == abjad.String.normalize(
        r'''
        digraph G {
        }
        ''')
    pickled = pickle.loads(pickle.dumps(graph))
    assert str(graph) == str(pickled)


def test_graphtools_GraphvizGraph_pickle_02():
    graph = abjad.graphtools.GraphvizGraph()
    graph.append(abjad.graphtools.GraphvizSubgraph())
    assert str(graph) == abjad.String.normalize(
        r'''
        digraph G {
            subgraph cluster_0 {
            }
        }
        ''')
    pickled = pickle.loads(pickle.dumps(graph))
    assert str(graph) == str(pickled)


def test_graphtools_GraphvizGraph_pickle_03():
    graph = abjad.graphtools.GraphvizGraph()
    graph.append(abjad.graphtools.GraphvizNode())
    graph.append(abjad.graphtools.GraphvizNode())
    assert str(graph) == abjad.String.normalize(
        r'''
        digraph G {
            node_0;
            node_1;
        }
        ''')
    pickled = pickle.loads(pickle.dumps(graph))
    assert str(graph) == str(pickled)


def test_graphtools_GraphvizGraph_pickle_04():
    graph = abjad.graphtools.GraphvizGraph()
    graph.append(abjad.graphtools.GraphvizNode())
    graph.append(abjad.graphtools.GraphvizNode())
    abjad.graphtools.GraphvizEdge().attach(graph[0], graph[1])
    assert str(graph) == abjad.String.normalize(
        r'''
        digraph G {
            node_0;
            node_1;
            node_0 -> node_1;
        }
        ''')
    pickled = pickle.loads(pickle.dumps(graph))
    assert str(graph) == str(pickled)


def test_graphtools_GraphvizGraph_pickle_05():
    graph = abjad.graphtools.GraphvizGraph()
    graph.append(abjad.graphtools.GraphvizSubgraph())
    graph[0].append(abjad.graphtools.GraphvizNode())
    graph[0].append(abjad.graphtools.GraphvizNode())
    graph[0].append(abjad.graphtools.GraphvizNode())
    graph[0].append(abjad.graphtools.GraphvizSubgraph())
    graph[0][-1].append(abjad.graphtools.GraphvizNode())
    graph.append(abjad.graphtools.GraphvizNode())
    abjad.graphtools.GraphvizEdge().attach(graph[0][1], graph[1])
    abjad.graphtools.GraphvizEdge().attach(graph[0][0], graph[0][-1][0])
    assert str(graph) == abjad.String.normalize(
        r'''
        digraph G {
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
        )
    pickled = pickle.loads(pickle.dumps(graph))
    assert str(graph) == str(pickled)
