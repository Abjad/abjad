import subprocess
from abjad.tools.datastructuretools import TreeContainer
from abjad.tools.graphtools.GraphvizMixin import GraphvizMixin
from abjad.tools.topleveltools import new


class GraphvizGraph(GraphvizMixin, TreeContainer):
    r'''A Graphviz graph.

    ..  container:: example

        ::

            >>> graph = abjad.graphtools.GraphvizGraph(name='G')

        Create other graphviz objects to insert into the graph:

        ::

            >>> cluster_0 = abjad.graphtools.GraphvizSubgraph(name='0')
            >>> cluster_1 = abjad.graphtools.GraphvizSubgraph(name='1')
            >>> a0 = abjad.graphtools.GraphvizNode(name='a0')
            >>> a1 = abjad.graphtools.GraphvizNode(name='a1')
            >>> a2 = abjad.graphtools.GraphvizNode(name='a2')
            >>> a3 = abjad.graphtools.GraphvizNode(name='a3')
            >>> b0 = abjad.graphtools.GraphvizNode(name='b0')
            >>> b1 = abjad.graphtools.GraphvizNode(name='b1')
            >>> b2 = abjad.graphtools.GraphvizNode(name='b2')
            >>> b3 = abjad.graphtools.GraphvizNode(name='b3')
            >>> start = abjad.graphtools.GraphvizNode(name='start')
            >>> end = abjad.graphtools.GraphvizNode(name='end')

        Group objects together into a tree:

        ::

            >>> graph.extend([cluster_0, cluster_1, start, end])
            >>> cluster_0.extend([a0, a1, a2, a3])
            >>> cluster_1.extend([b0, b1, b2, b3])

        Connect objects together with edges:

        ::

            >>> abjad.graphtools.GraphvizEdge().attach(start, a0)
            >>> abjad.graphtools.GraphvizEdge().attach(start, b0)
            >>> abjad.graphtools.GraphvizEdge().attach(a0, a1)
            >>> abjad.graphtools.GraphvizEdge().attach(a1, a2)
            >>> abjad.graphtools.GraphvizEdge().attach(a1, b3)
            >>> abjad.graphtools.GraphvizEdge().attach(a2, a3)
            >>> abjad.graphtools.GraphvizEdge().attach(a3, a0)
            >>> abjad.graphtools.GraphvizEdge().attach(a3, end)
            >>> abjad.graphtools.GraphvizEdge().attach(b0, b1)
            >>> abjad.graphtools.GraphvizEdge().attach(b1, b2)
            >>> abjad.graphtools.GraphvizEdge().attach(b2, b3)
            >>> abjad.graphtools.GraphvizEdge().attach(b2, a3)
            >>> abjad.graphtools.GraphvizEdge().attach(b3, end)

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

            >>> graph = abjad.graphtools.GraphvizGraph()
            >>> graph.append(abjad.graphtools.GraphvizSubgraph())
            >>> graph[0].append(abjad.graphtools.GraphvizNode())
            >>> graph[0].append(abjad.graphtools.GraphvizNode())
            >>> graph[0].append(abjad.graphtools.GraphvizNode())
            >>> graph[0].append(abjad.graphtools.GraphvizSubgraph())
            >>> graph[0][-1].append(abjad.graphtools.GraphvizNode())
            >>> graph.append(abjad.graphtools.GraphvizNode())
            >>> abjad.graphtools.GraphvizEdge().attach(graph[0][1], graph[1])
            >>> abjad.graphtools.GraphvizEdge().attach(graph[0][0], graph[0][-1][0])

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

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Graphviz'

    __slots__ = (
        '_attributes',
        '_edge_attributes',
        '_is_digraph',
        '_node_order',
        '_node_attributes',
        )

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
        GraphvizMixin.__init__(self, attributes=attributes)
        assert isinstance(edge_attributes, (dict, type(None)))
        assert isinstance(node_attributes, (dict, type(None)))
        self._verify_attributes(edge_attributes, '_edge_attributes')
        self._verify_attributes(node_attributes, '_node_attributes')
        self._is_digraph = bool(is_digraph)
        self._node_order = None

    ### SPECIAL METHODS ###

    def __copy__(self):
        r'''Copies GraphvizGraph.

        Returns copied graph.
        '''
        copied_node, edges, mapping = self._copy_with_memo(self)
        for edge in edges:
            head, tail = edge.head, edge.tail
            if head not in mapping or tail not in mapping:
                continue
            new_edge = new(edge)
            new_edge.attach(mapping[tail], mapping[head])
        return copied_node

    def __graph__(self, **keywords):
        r'''Gets graphviz graph.

        Returns graphviz graph.
        '''
        return self

    def __str__(self):
        r'''Graphviz format of Graphviz graph.

        Returns string.
        '''
        from abjad.tools import graphtools

        edges = set([])
        for node in self.nodes[1:]:
            if isinstance(node, (
                graphtools.GraphvizField,
                graphtools.GraphvizGroup,
                )):
                continue
            if isinstance(node, graphtools.GraphvizSubgraph):
                edges.update(node._edges)
            elif isinstance(node, graphtools.GraphvizNode):
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
        from abjad.tools import graphtools
        prototype = (
            graphtools.GraphvizSubgraph,
            graphtools.GraphvizNode,
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

        Returns true or false.
        '''
        return self._is_digraph

    @is_digraph.setter
    def is_digraph(self, argument):
        self._is_digraph = bool(argument)

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
        graphviz_format = str(self).encode('utf-8')
        process = subprocess.Popen(
            'unflatten -l 4'.split(),
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            )
        stdout, _ = process.communicate(graphviz_format)
        result = stdout.decode('utf-8')
        return result
