# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools import TreeContainer


class GraphvizGroup(TreeContainer):
    r'''A Graphviz struct field grouping.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Graphviz'

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        children=None,
        name=None,
        ):
        TreeContainer.__init__(
            self,
            children=children,
            name=name,
            )

    ### PRIVATE PROPERTIES ###

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
        if not self:
            return ''
        result = []
        for x in self:
            part = x._struct_format_contributions
            if part:
                result.append(part)
        result = ' | '.join(result)
        result = '{{ {} }}'.format(result)
        return result
