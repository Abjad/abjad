# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools import TreeNode


class GraphvizTableVerticalRule(TreeNode):
    r'''A Graphviz table vertical rule.
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
        r'''Gets string representation of Graphviz table vertical rule.

        Returns string.
        '''
        return '<VR/>'