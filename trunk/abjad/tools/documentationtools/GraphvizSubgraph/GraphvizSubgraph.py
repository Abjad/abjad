from abjad.tools.documentationtools.GraphvizGraph import GraphvizGraph


class GraphvizSubgraph(GraphvizGraph):
    '''A Graphviz cluster subgraph.'''

    ### INITIALIZER ###

    def __init__(self,
        attributes=None,
        children=None,
        edge_attributes=None,
        is_cluster=True,
        name=None,
        node_attributes=None
        ):
        GraphvizGraph.__init__(self,
            attributes=attributes,
            children=children,
            edge_attributes=edge_attributes,
            name=name,
            node_attributes=node_attributes
            )
        self.is_cluster = is_cluster
        self._edges = set([])

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _graphviz_format_pieces(self):
        result = []
        return result

    @property
    def _node_klass(self):
        from abjad.tools import documentationtools
        return (documentationtools.GraphvizSubgraph, documentationtools.GraphvizNode)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def canonical_name(self):
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
        return tuple(self._edges)

    ### READ/WRITE PUBLIC PROPERTIES ###

    @apply
    def is_cluster():
        def fget(self):
            return self._is_cluster
        def fset(self, arg):
            self._is_cluster = bool(arg)
        return property(**locals())
