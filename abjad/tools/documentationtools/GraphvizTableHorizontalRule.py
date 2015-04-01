# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools import TreeNode


class GraphvizTableHorizontalRule(TreeNode):
    r'''A Graphviz table horizontal rule.
    '''

    ### INITIALIZER ###

    def __init__(
        self,
        name=None,
        ):
        TreeNode.__init__(
            self,
            name=name,
            )

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of Graphviz table horizontal rule.

        Returns string.
        '''
        return '<HR/>'