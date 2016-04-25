# -*- coding: utf-8 -*-
from abjad.tools.documentationtools.GraphvizGraph import GraphvizGraph


class GraphvizSubgraph(GraphvizGraph):
    r'''A Graphviz cluster subgraph.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Graphviz'

    __slots__ = (
        '_is_cluster',
        '_edges',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        attributes=None,
        children=None,
        edge_attributes=None,
        is_cluster=True,
        name=None,
        node_attributes=None
        ):
        GraphvizGraph.__init__(
            self,
            attributes=attributes,
            children=children,
            edge_attributes=edge_attributes,
            name=name,
            node_attributes=node_attributes
            )
        self.is_cluster = is_cluster
        self._edges = set([])

    ### PRIVATE PROPERTIES ###

    @property
    def _graphviz_format_pieces(self):
        result = []
        return result

    @property
    def _node_class(self):
        from abjad.tools import documentationtools
        return (
            documentationtools.GraphvizSubgraph,
            documentationtools.GraphvizNode,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def canonical_name(self):
        r'''Canonical name of Graphviz subgraph.

        Returns string.
        '''
        if self.name is not None:
            if self.is_cluster:
                return 'cluster_' + self.name
            return self.name
        prefix = 'subgraph_'
        if self.is_cluster:
            prefix = 'cluster_'
        return prefix + '_'.join(str(x) for x in self.graph_order)

    @property
    def edges(self):
        r'''Edges of Graphviz subgraph.

        Returns tuple.
        '''
        return tuple(self._edges)

    @property
    def is_cluster(self):
        r'''Is true when Graphviz subgraph is a cluster. Otherwise false.

        Returns true or false.
        '''
        return self._is_cluster

    @is_cluster.setter
    def is_cluster(self, arg):
        self._is_cluster = bool(arg)
