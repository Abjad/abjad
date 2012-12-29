import copy
from abjad.tools.datastructuretools import TreeContainer
from abjad.tools.documentationtools.GraphvizObject import GraphvizObject


class GraphvizGraph(TreeContainer, GraphvizObject):
    '''Abjad model of a Graphviz graph:

    ::

        >>> graph = documentationtools.GraphvizGraph(name='G')

    Create other graphviz objects to insert into the graph:

    ::

        >>> cluster_0 = documentationtools.GraphvizCluster(name='cluster_0')
        >>> cluster_1 = documentationtools.GraphvizCluster(name='cluster_1')
        >>> a0 = documentationtools.GraphvizNode(name='a0')
        >>> a1 = documentationtools.GraphvizNode(name='a1')
        >>> a2 = documentationtools.GraphvizNode(name='a2')
        >>> a3 = documentationtools.GraphvizNode(name='a3')
        >>> b0 = documentationtools.GraphvizNode(name='b0')
        >>> b1 = documentationtools.GraphvizNode(name='b1')
        >>> b2 = documentationtools.GraphvizNode(name='b2')
        >>> b3 = documentationtools.GraphvizNode(name='b3')
        >>> start = documentationtools.GraphvizNode(name='start')
        >>> end = documentationtools.GraphvizNode(name='end')

    Group objects together into a tree:

    ::

        >>> graph.extend([cluster_0, cluster_1, start, end])
        >>> cluster_0.extend([a0, a1, a2, a3])
        >>> cluster_1.extend([b0, b1, b2, b3])

    Connect objects together with edges:

    ::

        >>> edge = documentationtools.GraphvizEdge()(start, a0)
        >>> edge = documentationtools.GraphvizEdge()(start, b0)
        >>> edge = documentationtools.GraphvizEdge()(a0, a1)
        >>> edge = documentationtools.GraphvizEdge()(a1, a2)
        >>> edge = documentationtools.GraphvizEdge()(a1, b3)
        >>> edge = documentationtools.GraphvizEdge()(a2, a3)
        >>> edge = documentationtools.GraphvizEdge()(a3, a0)
        >>> edge = documentationtools.GraphvizEdge()(a3, end)
        >>> edge = documentationtools.GraphvizEdge()(b0, b1)
        >>> edge = documentationtools.GraphvizEdge()(b1, b2)
        >>> edge = documentationtools.GraphvizEdge()(b2, b3)
        >>> edge = documentationtools.GraphvizEdge()(b2, a3)
        >>> edge = documentationtools.GraphvizEdge()(b3, end)

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

    Access the computed graphviz format of the graph:

    ::

        >>> print graph.graphviz_format
        digraph "G" {
            subgraph "cluster_0" {
                color="lightgrey";
                label="process #1";
                style="filled";
                node [color="white", style="filled"];
                "a0";
                "a1";
                "a2";
                "a3";
                "a0" -> "a1";
                "a1" -> "a2";
                "a2" -> "a3";
                "a3" -> "a0";
            }
            subgraph "cluster_1" {
                color="blue";
                label="process #2";
                node [style="filled"];
                "b0";
                "b1";
                "b2";
                "b3";
                "b0" -> "b1";
                "b1" -> "b2";
                "b2" -> "b3";
            }
            "start" [shape="Mdiamond"];
            "end" [shape="Msquare"];
            "a1" -> "b3";
            "a3" -> "end";
            "b2" -> "a3";
            "b3" -> "end";
            "start" -> "a0";
            "start" -> "b0";
        }

    View the graph:

    ::

        >>> iotools.graph(graph) # doctest: +SKIP

    Return GraphvizGraph instance.
    '''

    ### INITIALIZER ###

    def __init__(self,
        attributes=None,
        children=None,
        edge_attributes=None,
        is_digraph=True,
        name=None,
        node_attributes=None
        ):
        TreeContainer.__init__(self, children=children, name=name)
        GraphvizObject.__init__(self, attributes=attributes)
        assert isinstance(edge_attributes, (dict, type(None)))
        assert isinstance(node_attributes, (dict, type(None)))
        if edge_attributes is None:
            self._edge_attributes = {}
        else:
            self._edge_attributes = copy.copy(edge_attributes)
        if node_attributes is None:
            self._node_attributes = {}
        else:
            self._node_attributes = copy.copy(node_attributes)
        self._is_digraph = bool(is_digraph)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _node_klass(self):
        from abjad.tools import documentationtools
        return (documentationtools.GraphvizCluster, documentationtools.GraphvizNode)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def edge_attributes(self):
        return self._edge_attributes

    @property
    def graphviz_format(self):
        edges = set([])
        for node in self.nodes[1:]:
            edges.update(node._edges)

        edge_parents = {}
        for edge in edges:
            last_parent = None
            tail_parentage = list(edge.tail.proper_parentage)
            head_parentage = list(edge.head.proper_parentage)
            while len(tail_parentage) and len(head_parentage) and \
                tail_parentage[-1] is head_parentage[-1]:
                last_parent = tail_parentage[-1]
                tail_parentage.pop()
                head_parentage.pop()
            if last_parent is None:
                raise Exception
            if last_parent not in edge_parents:
                edge_parents[last_parent] = []
            edge_parents[last_parent].append(edge)

        result = ['digraph {} {{'.format(self.name)]

        def recurse(node, indent=0, prefix='subgraph'):
            indent_one = indent * '\t'
            indent_two = (indent + 1) * '\t'
            result = ['{}{} "{}" {{'.format(indent_one, prefix, node.name)]
            for name, value in sorted(node.attributes.items()):
                result.append('{}{};'.format(indent_two, self._format_attribute(name, value)))
            if len(node.node_attributes):
                result.append('{}node {};'.format(
                    indent_two, self._format_attribute_list(node.node_attributes)))
            if len(node.edge_attributes):
                result.append('{}edge {};'.format(
                    indent_two, self._format_attribute_list(node.edge_attributes)))
            for child in node:
                if isinstance(child, type(self)):
                    result.extend(recurse(child, indent=indent+1))
                else:
                    result.append(indent_two + child._graphviz_format_contributions)
            if node in edge_parents:
                edge_contributions = []
                for edge in edge_parents[node]:
                    edge_contributions.append(indent_two + edge._graphviz_format_contributions)
                edge_contributions.sort()
                result.extend(edge_contributions)
            result.append('{}}}'.format(indent_one))
            return result

        if self.is_digraph:
            return '\n'.join(recurse(self, indent=0, prefix='digraph'))
        return '\n'.join(recurse(self, indent=0, prefix='graph'))

    @property
    def node_attributes(self):
        return self._node_attributes

    ### READ/WRITE PUBLIC PROPERTIES ###

    @apply
    def is_digraph():
        def fget(self):
            return self._is_digraph
        def fset(self, arg):
            self._is_digraph = bool(arg)
        return property(**locals())

