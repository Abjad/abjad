import copy
from abjad.tools.datastructuretools import TreeContainer


class GraphvizGraph(TreeContainer):
    '''Abjad model of a Graphviz graph:

    ::

        >>> graph = graphviztools.GraphvizGraph(name='G')

    Create other graphviz objects to insert into the graph:

    ::

        >>> cluster_0 = graphviztools.GraphvizCluster(name='cluster_0')
        >>> cluster_1 = graphviztools.GraphvizCluster(name='cluster_1')
        >>> a0 = graphviztools.GraphvizNode(name='a0')
        >>> a1 = graphviztools.GraphvizNode(name='a1')
        >>> a2 = graphviztools.GraphvizNode(name='a2')
        >>> a3 = graphviztools.GraphvizNode(name='a3')
        >>> b0 = graphviztools.GraphvizNode(name='b0')
        >>> b1 = graphviztools.GraphvizNode(name='b1')
        >>> b2 = graphviztools.GraphvizNode(name='b2')
        >>> b3 = graphviztools.GraphvizNode(name='b3')
        >>> start = graphviztools.GraphvizNode(name='start')
        >>> end = graphviztools.GraphvizNode(name='end')

    Group objects together into a tree:

    ::

        >>> graph.extend([cluster_0, cluster_1, start, end])
        >>> cluster_0.extend([a0, a1, a2, a3])
        >>> cluster_1.extend([b0, b1, b2, b3])

    Connect objects together with edges:

    ::

        >>> edge = graphviztools.GraphvizEdge()(start, a0)
        >>> edge = graphviztools.GraphvizEdge()(start, b0)
        >>> edge = graphviztools.GraphvizEdge()(a0, a1)
        >>> edge = graphviztools.GraphvizEdge()(a1, a2)
        >>> edge = graphviztools.GraphvizEdge()(a1, b3)
        >>> edge = graphviztools.GraphvizEdge()(a2, a3)
        >>> edge = graphviztools.GraphvizEdge()(a3, a0)
        >>> edge = graphviztools.GraphvizEdge()(a3, end)
        >>> edge = graphviztools.GraphvizEdge()(b0, b1)
        >>> edge = graphviztools.GraphvizEdge()(b1, b2)
        >>> edge = graphviztools.GraphvizEdge()(b2, b3)
        >>> edge = graphviztools.GraphvizEdge()(b2, a3)
        >>> edge = graphviztools.GraphvizEdge()(b3, end)

    Add attributes to style the objects:

    ::

        >>> cluster_0.attributes['style'] = 'filled'
        >>> cluster_0.attributes['color'] = 'lightgrey'
        >>> cluster_0.attributes['label'] = 'process #1'
        >>> cluster_0.node_attributes['style'] = 'filled'
        >>> cluster_0.node_attributes['color'] = 'white'
        >>> cluster_1.attributes['color'] = 'blue'
        >>> cluster_1.attributes['label'] = 'process #2'
        >>> cluster_1.node_attributes['style'] = 'filled'
        >>> start.attributes['shape'] = 'Mdiamond'
        >>> end.attributes['shape'] = 'Msquare'

    Return GraphvizGraph instance.
    '''

    ### INITIALIZER ###

    def __init__(self,
        attributes=None,
        children=None,
        edge_attributes=None,
        name=None,
        node_attributes=None
        ):
        TreeContainer.__init__(self, children=children, name=name)
        assert isinstance(attributes, (dict, type(None)))
        assert isinstance(edge_attributes, (dict, type(None)))
        assert isinstance(node_attributes, (dict, type(None)))
        if attributes is None:
            self._attributes = {}
        else:
            self._attributes = copy.copy(attributes)
        if edge_attributes is None:
            self._edge_attributes = {}
        else:
            self._edge_attributes = copy.copy(edge_attributes)
        if node_attributes is None:
            self._node_attributes = {}
        else:
            self._node_attributes = copy.copy(node_attributes)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _node_klass(self):
        from experimental.tools import graphviztools
        return (graphviztools.GraphvizCluster, graphviztools.GraphvizNode)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attributes(self):
        return self._attributes

    @property
    def edge_attributes(self):
        return self._edge_attributes

    @property
    def graphviz_format(self):
        result = []
        return result

    @property
    def node_attributes(self):
        return self._node_attributes

