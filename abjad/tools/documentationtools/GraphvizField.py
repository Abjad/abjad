# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools import TreeNode


class GraphvizField(TreeNode):
    r'''A Graphviz struct field.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Graphviz'

    __slots__ = (
        '_edges',
        '_label',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        label=None,
        name=None,
        ):
        TreeNode.__init__(self, name=name)
        self._label = label
        self._edges = set([])

    ### PRIVATE PROPERTIES ###

    @property
    def _struct_format_contributions(self):
        result = '<{}>'.format(self.field_name)
        if self.label:
            result = '{} {}'.format(result, self.label)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def canonical_name(self):
        r'''Gets field canonical name.
        '''
        canonical_name = '{}:{}'.format(
            self.struct.canonical_name,
            self.field_name,
            )
        return canonical_name

    @property
    def edges(self):
        r'''Gets edges of Graphviz struct field.
        '''
        return tuple(self._edges)

    @property
    def field_name(self):
        r'''Gets the field name.
        '''
        graph_order = self.graph_order
        struct = self.struct
        if struct is not None:
            struct_graph_order = struct.graph_order
            graph_order = graph_order[len(struct_graph_order):]
        return 'f_' + '_'.join(str(x) for x in graph_order)

    @property
    def label(self):
        r'''Gets the field label.
        '''
        return self._label

    @property
    def struct(self):
        r'''Gets the parent struct.
        '''
        from abjad.tools import documentationtools
        parent = self.parent
        while parent is not None:
            if isinstance(parent, documentationtools.GraphvizNode):
                return parent
            parent = parent.parent
