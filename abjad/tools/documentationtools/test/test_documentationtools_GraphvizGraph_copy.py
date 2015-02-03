# -*- encoding: utf-8 -*-
import copy
import pytest
from abjad.tools import documentationtools


@pytest.skip('FIXME')
def test_documentationtools_GraphvizGraph_copy_01():
    graph = documentationtools.GraphvizGraph()
    graph.append(documentationtools.GraphvizSubgraph())
    graph[0].append(documentationtools.GraphvizNode())
    graph[0].append(documentationtools.GraphvizNode())
    graph[0].append(documentationtools.GraphvizNode())
    graph[0].append(documentationtools.GraphvizSubgraph())
    graph[0][-1].append(documentationtools.GraphvizNode())
    graph.append(documentationtools.GraphvizNode())
    documentationtools.GraphvizEdge()(
        graph[0][1],
        graph[1],
        )
    documentationtools.GraphvizEdge()(
        graph[0][0],
        graph[0][-1][0],
        )

    new_graph = copy.deepcopy(graph)

    assert str(graph) == str(new_graph)