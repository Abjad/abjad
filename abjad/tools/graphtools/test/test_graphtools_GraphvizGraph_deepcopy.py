# -*- coding: utf-8 -*-
import copy
from abjad.tools import graphtools
from abjad.tools import stringtools


def test_documentationtools_GraphvizGraph_deepcopy_01():
    graph = graphtools.GraphvizGraph()
    assert str(graph) == stringtools.normalize(
        r'''
        digraph G {
        }
        ''')
    copied = copy.deepcopy(graph)
    assert str(graph) == str(copied)


def test_documentationtools_GraphvizGraph_deepcopy_02():
    graph = graphtools.GraphvizGraph()
    graph.append(graphtools.GraphvizSubgraph())
    assert str(graph) == stringtools.normalize(
        r'''
        digraph G {
            subgraph cluster_0 {
            }
        }
        ''')
    copied = copy.deepcopy(graph)
    assert str(graph) == str(copied)


def test_documentationtools_GraphvizGraph_deepcopy_03():
    graph = graphtools.GraphvizGraph()
    graph.append(graphtools.GraphvizNode())
    graph.append(graphtools.GraphvizNode())
    assert str(graph) == stringtools.normalize(
        r'''
        digraph G {
            node_0;
            node_1;
        }
        ''')
    copied = copy.deepcopy(graph)
    assert str(graph) == str(copied)


def test_documentationtools_GraphvizGraph_deepcopy_04():
    graph = graphtools.GraphvizGraph()
    graph.append(graphtools.GraphvizNode())
    graph.append(graphtools.GraphvizNode())
    graphtools.GraphvizEdge().attach(graph[0], graph[1])
    assert str(graph) == stringtools.normalize(
        r'''
        digraph G {
            node_0;
            node_1;
            node_0 -> node_1;
        }
        ''')
    copied = copy.deepcopy(graph)
    assert str(graph) == str(copied)


def test_documentationtools_GraphvizGraph_deepcopy_05():
    graph = graphtools.GraphvizGraph()
    graph.append(graphtools.GraphvizSubgraph())
    graph[0].append(graphtools.GraphvizNode())
    graph[0].append(graphtools.GraphvizNode())
    graph[0].append(graphtools.GraphvizNode())
    graph[0].append(graphtools.GraphvizSubgraph())
    graph[0][-1].append(graphtools.GraphvizNode())
    graph.append(graphtools.GraphvizNode())
    graphtools.GraphvizEdge().attach(graph[0][1], graph[1])
    graphtools.GraphvizEdge().attach(graph[0][0], graph[0][-1][0])
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
    copied = copy.deepcopy(graph)
    assert str(graph) == str(copied)
