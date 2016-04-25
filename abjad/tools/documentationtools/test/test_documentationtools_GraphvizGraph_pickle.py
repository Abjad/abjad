# -*- coding: utf-8 -*-
import pickle
from abjad.tools import documentationtools
from abjad.tools import stringtools


def test_documentationtools_GraphvizGraph_pickle_01():
    graph = documentationtools.GraphvizGraph()
    assert str(graph) == stringtools.normalize(
        r'''
        digraph G {
        }
        ''')
    pickled = pickle.loads(pickle.dumps(graph))
    assert str(graph) == str(pickled)


def test_documentationtools_GraphvizGraph_pickle_02():
    graph = documentationtools.GraphvizGraph()
    graph.append(documentationtools.GraphvizSubgraph())
    assert str(graph) == stringtools.normalize(
        r'''
        digraph G {
            subgraph cluster_0 {
            }
        }
        ''')
    pickled = pickle.loads(pickle.dumps(graph))
    assert str(graph) == str(pickled)


def test_documentationtools_GraphvizGraph_pickle_03():
    graph = documentationtools.GraphvizGraph()
    graph.append(documentationtools.GraphvizNode())
    graph.append(documentationtools.GraphvizNode())
    assert str(graph) == stringtools.normalize(
        r'''
        digraph G {
            node_0;
            node_1;
        }
        ''')
    pickled = pickle.loads(pickle.dumps(graph))
    assert str(graph) == str(pickled)


def test_documentationtools_GraphvizGraph_pickle_04():
    graph = documentationtools.GraphvizGraph()
    graph.append(documentationtools.GraphvizNode())
    graph.append(documentationtools.GraphvizNode())
    documentationtools.GraphvizEdge().attach(graph[0], graph[1])
    assert str(graph) == stringtools.normalize(
        r'''
        digraph G {
            node_0;
            node_1;
            node_0 -> node_1;
        }
        ''')
    pickled = pickle.loads(pickle.dumps(graph))
    assert str(graph) == str(pickled)


def test_documentationtools_GraphvizGraph_pickle_05():
    graph = documentationtools.GraphvizGraph()
    graph.append(documentationtools.GraphvizSubgraph())
    graph[0].append(documentationtools.GraphvizNode())
    graph[0].append(documentationtools.GraphvizNode())
    graph[0].append(documentationtools.GraphvizNode())
    graph[0].append(documentationtools.GraphvizSubgraph())
    graph[0][-1].append(documentationtools.GraphvizNode())
    graph.append(documentationtools.GraphvizNode())
    documentationtools.GraphvizEdge().attach(graph[0][1], graph[1])
    documentationtools.GraphvizEdge().attach(graph[0][0], graph[0][-1][0])
    assert str(graph) == stringtools.normalize(
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
