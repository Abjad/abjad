# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools import TreeContainer


class GraphvizTableRow(TreeContainer):
    r'''A Graphviz table row.
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

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of Graphviz table row.

        Returns string.
        '''
        result = []
        result.append('<TR>')
        for x in self:
            result.append('    ' + str(x))
        result.append('</TR>')
        result = '\n'.join(result)
        return result

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self):
        from abjad.tools import documentationtools
        prototype = (
            documentationtools.GraphvizTableCell,
            documentationtools.GraphvizTableVerticalRule,
            )
        return prototype
