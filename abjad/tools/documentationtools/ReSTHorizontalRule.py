# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TreeNode import TreeNode


class ReSTHorizontalRule(TreeNode):
    r'''A ReST horizontal rule.

    ::

        >>> rule = documentationtools.ReSTHorizontalRule()
        >>> rule
        ReSTHorizontalRule()

    ::

        >>> print rule.rest_format
        --------

    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _rest_format_contributions(self):
        return ['--------']

    ### PUBLIC PROPERTIES ###

    @property
    def rest_format(self):
        r'''ReST format of ReSt horizontal rule.

        Returns text.
        '''
        return '\n'.join(self._rest_format_contributions)
