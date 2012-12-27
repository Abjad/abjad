from experimental.tools.graphviztools.GraphvizGraph import GraphvizGraph


class GraphvizCluster(GraphvizGraph):
    '''A Graphviz cluster subgraph.'''

    ### INITIALIZER ###

    def __init__(self,
        attributes=None,
        children=None,
        edge_attributes=None,
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
        self._edges = set([])

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _graphviz_format_pieces(self):
        result = []
        return result

    @property
    def _node_klass(self):
        from experimental.tools import graphviztools
        return (graphviztools.GraphvizCluster, graphviztools.GraphvizNode)

    ### READ-ONLY PUBLIC PROPERTIES ###
 
    @property
    def edges(self):
        return tuple(self._edges)


