# -*- coding: utf-8 -*-


def make_reference_manual_graphviz_graph(graph):
    r'''Make a GraphvizGraph instance suitable for use in the
    Abjad reference manual.

    Returns GraphvizGraph instance.
    '''

    from abjad.tools import documentationtools

    if not isinstance(graph, documentationtools.GraphvizGraph):
        try:
            graph = graph.__graph__()
        except:
            return graph
    graph.attributes['size'] = "8.0, 12.0"
    graph.node_attributes['fontsize'] = 10
    return graph
