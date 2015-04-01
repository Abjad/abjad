# -*- encoding: utf-8 -*-
import subprocess
from abjad.tools.datastructuretools import TreeContainer
from abjad.tools.documentationtools.GraphvizObject import GraphvizObject


class GraphvizGraph(TreeContainer, GraphvizObject):
    r'''A Graphviz graph.

    ::

        >>> graph = documentationtools.GraphvizGraph(name='G')

    Create other graphviz objects to insert into the graph:

    ::

        >>> cluster_0 = documentationtools.GraphvizSubgraph(name='0')
        >>> cluster_1 = documentationtools.GraphvizSubgraph(name='1')
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
        >>> cluster_1.node_attributes['style'] = ('filled', 'rounded')
        >>> start.attributes['shape'] = 'Mdiamond'
        >>> end.attributes['shape'] = 'Msquare'

    Access the computed graphviz format of the graph:

    ::

        >>> print(str(graph))
        digraph G {
            subgraph cluster_0 {
                graph [color=lightgrey,
                    label="process #1",
                    style=filled];
                node [color=white,
                    style=filled];
                a0;
                a1;
                a2;
                a3;
                a0 -> a1;
                a1 -> a2;
                a2 -> a3;
                a3 -> a0;
            }
            subgraph cluster_1 {
                graph [color=blue,
                    label="process #2"];
                node [style="filled, rounded"];
                b0;
                b1;
                b2;
                b3;
                b0 -> b1;
                b1 -> b2;
                b2 -> b3;
            }
            start [shape=Mdiamond];
            end [shape=Msquare];
            a1 -> b3;
            a3 -> end;
            b2 -> a3;
            b3 -> end;
            start -> a0;
            start -> b0;
        }

    View the graph:

    ::

        >>> topleveltools.graph(graph) # doctest: +SKIP

    Graphs can also be created without defining names.  Canonical names
    will be automatically determined for all members whose `name` is None:

    ::

        >>> graph = documentationtools.GraphvizGraph()
        >>> graph.append(documentationtools.GraphvizSubgraph())
        >>> graph[0].append(documentationtools.GraphvizNode())
        >>> graph[0].append(documentationtools.GraphvizNode())
        >>> graph[0].append(documentationtools.GraphvizNode())
        >>> graph[0].append(documentationtools.GraphvizSubgraph())
        >>> graph[0][-1].append(documentationtools.GraphvizNode())
        >>> graph.append(documentationtools.GraphvizNode())
        >>> edge = documentationtools.GraphvizEdge()(graph[0][1], graph[1])
        >>> edge = documentationtools.GraphvizEdge()(
        ...     graph[0][0], graph[0][-1][0])

    ::

        >>> print(str(graph))
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

    ### INITIALIZER ###

    def __init__(
        self,
        attributes=None,
        children=None,
        edge_attributes=None,
        is_digraph=True,
        name=None,
        node_attributes=None,
        ):
        TreeContainer.__init__(self, children=children, name=name)
        GraphvizObject.__init__(self, attributes=attributes)
        assert isinstance(edge_attributes, (dict, type(None)))
        assert isinstance(node_attributes, (dict, type(None)))
        self._verify_attributes(edge_attributes, '_edge_attributes')
        self._verify_attributes(node_attributes, '_node_attributes')
        self._is_digraph = bool(is_digraph)
        self._node_order = None

    ### SPECIAL METHODS ###

    def __graph__(self, **kwargs):
        r'''Gets graphviz graph.

        Returns graphviz graph.
        '''
        return self

    def __str__(self):
        r'''Graphviz format of Graphviz graph.

        Returns string.
        '''
        from abjad.tools import documentationtools

        edges = set([])
        for node in self.nodes[1:]:
            if isinstance(node, (
                documentationtools.GraphvizField,
                documentationtools.GraphvizGroup,
                )):
                continue
            if isinstance(node, documentationtools.GraphvizSubgraph):
                edges.update(node._edges)
            elif isinstance(node, documentationtools.GraphvizNode):
                edges.update(node.all_edges)
        edges = sorted(edges, key=lambda edge: (
            edge.tail.graph_order, edge.head.graph_order,
            ))

        edge_parents = {}
        for edge in edges:
            highest_parent = edge._get_highest_parent()
            if highest_parent not in edge_parents:
                edge_parents[highest_parent] = []
            edge_parents[highest_parent].append(edge)

        visited_edges = set()

        def recurse(node, indent=0, prefix='subgraph'):
            indent_one = indent * '    '
            indent_two = (indent + 1) * '    '
            result = []

            string = '{}{} {} {{'.format(
                indent_one,
                prefix,
                self._format_value(node.canonical_name)
                )
            result.append(string)

            if len(node.attributes):
                contributions = self._format_attribute_list(node.attributes)
                contributions[0] = 'graph {}'.format(contributions[0])
                result.extend(indent_two + x for x in contributions)
            if len(node.node_attributes):
                contributions = \
                    self._format_attribute_list(node.node_attributes)
                contributions[0] = 'node {}'.format(contributions[0])
                result.extend(indent_two + x for x in contributions)
            if len(node.edge_attributes):
                contributions = \
                    self._format_attribute_list(node.edge_attributes)
                contributions[0] = 'edge {}'.format(contributions[0])
                result.extend(indent_two + x for x in contributions)

            if indent == 0 and self._node_order:
                for node_name in self._node_order:
                    result.append('{}{};'.format(indent_two, node_name))

            for child in node:
                if isinstance(child, type(self)):
                    lines = recurse(child, indent=indent + 1)
                else:
                    lines = (indent_two + line for line in
                        child._graphviz_format_contributions)
                result.extend(lines)

            if node in edge_parents:
                edge_contributions = []
                for edge in edge_parents[node]:
                    if edge in visited_edges:
                        continue
                    for line in edge._graphviz_format_contributions:
                        edge_contributions.append(indent_two + line)
                    visited_edges.add(edge)
                result.extend(edge_contributions)

            result.append('{}}}'.format(indent_one))

            return result

        if self.is_digraph:
            return '\n'.join(recurse(self, indent=0, prefix='digraph'))
        return '\n'.join(recurse(self, indent=0, prefix='graph'))

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self):
        from abjad.tools import documentationtools
        prototype = (
            documentationtools.GraphvizSubgraph,
            documentationtools.GraphvizNode,
            )
        return prototype

    ### PUBLIC PROPERTIES ###

    @property
    def canonical_name(self):
        r'''Canonical name of Graphviz graph.

        Returns string.
        '''
        if self.name is not None:
            return self.name
        return 'G'

    @property
    def edge_attributes(self):
        r'''Edge attributes of Graphviz graph.
        '''
        return self._edge_attributes

    @property
    def is_digraph(self):
        r'''Is true when Graphviz graph is a digraph. Otherwise false.

        Returns boolean.
        '''
        return self._is_digraph

    @is_digraph.setter
    def is_digraph(self, arg):
        self._is_digraph = bool(arg)

    @property
    def node_attributes(self):
        r'''Node attributes of Graphviz graph.
        '''
        return self._node_attributes

    @property
    def unflattened_graphviz_format(self):
        r'''Unflattened Graphviz format of Graphviz graph.

        Returns list.
        '''
        from abjad.tools import systemtools
        assert systemtools.IOManager.find_executable(
            'unflatten'), 'Cannot find `unflatten` command-line tool.'
        graphviz_format = str(self)
        process = subprocess.Popen('unflatten -l 4'.split(),
            shell=False,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )
        result = process.communicate(graphviz_format)[0]
        return result