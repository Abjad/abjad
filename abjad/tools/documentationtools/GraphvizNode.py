# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools import TreeContainer
from abjad.tools.documentationtools.GraphvizObject import GraphvizObject


class GraphvizNode(TreeContainer, GraphvizObject):
    r'''A Graphviz node.
    '''

    ### INITIALIZER ###

    def __init__(
        self,
        attributes=None,
        children=None,
        name=None,
        ):
        self._children = []
        TreeContainer.__init__(
            self,
            children=children,
            name=name,
            )
        GraphvizObject.__init__(
            self,
            attributes=attributes,
            )
        self._edges = set([])

    ### PRIVATE PROPERTIES ###

    @property
    def _graphviz_format_contributions(self):
        node_def = self._format_value(self.canonical_name)
        attributes = self.attributes
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
        for node in self.nodes[1:]:
            if isinstance(node, documentationtools.GraphvizGroup):
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
        return 'node_' + '_'.join(str(x) for x in self.graph_order)

    @property
    def edges(self):
        r'''Edges of Graphviz node.

        Returns tuple.
        '''
        return tuple(self._edges)