# -*- encoding: utf-8 -*-
import copy
from abjad.tools import documentationtools
from abjad.tools import systemtools


def test_documentationtools_GraphvizGraph_copy_01():
    graph = documentationtools.GraphvizGraph()
    assert str(graph) == systemtools.TestManager.clean_string(
        r'''
        digraph G {
        }
        ''')
    copied = copy.copy(graph)
    assert str(graph) == str(copied)


def test_documentationtools_GraphvizGraph_copy_02():
    graph = documentationtools.GraphvizGraph()
    graph.append(documentationtools.GraphvizSubgraph())
    assert str(graph) == systemtools.TestManager.clean_string(
        r'''
        digraph G {
            subgraph cluster_0 {
            }
        }
        ''')
    copied = copy.copy(graph)
    assert str(graph) == str(copied)


def test_documentationtools_GraphvizGraph_copy_03():
    graph = documentationtools.GraphvizGraph()
    graph.append(documentationtools.GraphvizNode())
    graph.append(documentationtools.GraphvizNode())
    assert str(graph) == systemtools.TestManager.clean_string(
        r'''
        digraph G {
            node_0;
            node_1;
        }
        ''')
    copied = copy.copy(graph)
    assert str(graph) == str(copied)


def test_documentationtools_GraphvizGraph_copy_04():
    graph = documentationtools.GraphvizGraph()
    graph.append(documentationtools.GraphvizNode())
    graph.append(documentationtools.GraphvizNode())
    edge = documentationtools.GraphvizEdge()(graph[0], graph[1])
    assert str(graph) == systemtools.TestManager.clean_string(
        r'''
        digraph G {
            node_0;
            node_1;
            node_0 -> node_1;
        }
        ''')
    copied = copy.copy(graph)
    assert str(graph) == str(copied)


def test_documentationtools_GraphvizGraph_copy_05():
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
    assert str(graph) == systemtools.TestManager.clean_string(
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
    copied = copy.copy(graph)
    assert str(graph) == str(copied)


def test_documentationtools_GraphvizGraph_copy_06():
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
    copied = copy.copy(graph[0])
    assert str(copied) == systemtools.TestManager.clean_string(
        r'''
        digraph cluster_ {
            node_0;
            node_1;
            node_2;
            subgraph cluster_3 {
                node_3_0;
            }
            node_0 -> node_3_0;
        }
        ''')
    assert copied.parent is None