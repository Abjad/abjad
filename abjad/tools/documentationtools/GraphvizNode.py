# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools import TreeContainer
from abjad.tools.documentationtools.GraphvizMixin import GraphvizMixin


class GraphvizNode(GraphvizMixin, TreeContainer):
    r'''A Graphviz node.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Graphviz'

    __slots__ = (
        '_attributes',
        '_edges',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        attributes=None,
        children=None,
        name=None,
        ):
        TreeContainer.__init__(
            self,
            children=children,
            name=name,
            )
        GraphvizMixin.__init__(
            self,
            attributes=attributes,
            )
        self._edges = set([])

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of Graphviz node.

        Returns string.
        '''
        result = self._graphviz_format_contributions
        result = '\n'.join(result)
        return result

    ### PUBLIC METHODS ###

    def attach(self, other):
        r'''Attaches node to attachable Graphviz object.

        ::

            >>> my_graph = documentationtools.GraphvizGraph()
            >>> node_one = documentationtools.GraphvizNode(attributes={'label': 'One'})
            >>> node_two = documentationtools.GraphvizNode(attributes={'label': 'Two'})
            >>> my_graph.extend([node_one, node_two])
            >>> edge = node_one.attach(node_two)
            >>> graph(my_graph)  # doctest: +SKIP

        ..  doctest::

            >>> print(str(my_graph))
            digraph G {
                node_0 [label=One];
                node_1 [label=Two];
                node_0 -> node_1;
            }

        Returns GraphvizEdge.
        '''
        from abjad.tools import documentationtools
        edge = documentationtools.GraphvizEdge()
        edge.attach(self, other)
        return edge

    ### PRIVATE PROPERTIES ###

    @property
    def _graphviz_format_contributions(self):
        from abjad.tools import documentationtools

        node_def = self._format_value(self.canonical_name)
        attributes = self.attributes

        if len(self) == 1 and not isinstance(self[0], (
            documentationtools.GraphvizField,
            documentationtools.GraphvizGroup,
            )):
            attributes['label'] = self[0]
        elif len(self):
            struct_format_contributions = self._struct_format_contributions
            if struct_format_contributions:
                attributes['label'] = struct_format_contributions

        if len(attributes):
            result = []
            result.extend(self._format_attribute_list(attributes))
            result[0] = '{} {}'.format(node_def, result[0])
            return result

        return [node_def + ';']

    @property
    def _node_class(self):
        from abjad.tools import documentationtools
        prototype = (
            documentationtools.GraphvizField,
            documentationtools.GraphvizGroup,
            documentationtools.GraphvizTable,
            )
        return prototype

    @property
    def _struct_format_contributions(self):
        result = []
        for x in self:
            part = x._struct_format_contributions
            if part:
                result.append(part)
        result = ' | '.join(result)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def all_edges(self):
        r'''Gets edges of this node and those of any field in its field
        subtree.
        '''
        from abjad.tools import documentationtools
        edges = set(self.edges)
        prototype = (
            documentationtools.GraphvizGroup,
            documentationtools.GraphvizTable,
            documentationtools.GraphvizTableCell,
            documentationtools.GraphvizTableRow,
            documentationtools.GraphvizTableHorizontalRule,
            documentationtools.GraphvizTableVerticalRule,
            )
        for node in self.nodes[1:]:
            if isinstance(node, prototype):
                continue
            edges.update(node.edges)
        return tuple(edges)

    @property
    def canonical_name(self):
        r'''Canonical name of Graphviz node.

        Returns string.
        '''
        if self.name is not None:
            return self.name
        if self.graph_order:
            return 'node_' + '_'.join(str(x) for x in self.graph_order)
        return 'node_0'

    @property
    def edges(self):
        r'''Edges of Graphviz node.

        Returns tuple.
        '''
        return tuple(self._edges)
