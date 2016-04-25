# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools.TreeNode import TreeNode


class ReSTAutosummaryItem(TreeNode):
    r'''A ReST autosummary item.

    ::

        >>> item = documentationtools.ReSTAutosummaryItem(
        ...     text='abjad.tools.scoretools.Note')
        >>> item
        ReSTAutosummaryItem(
            text='abjad.tools.scoretools.Note'
            )

    ::

        >>> print(item.rest_format)
        abjad.tools.scoretools.Note

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'reStructuredText'

    ### INITIALIZER ###

    def __init__(self, name=None, text='foo'):
        TreeNode.__init__(self, name)
        self.text = text

    ### PRIVATE PROPERTIES ###

    @property
    def _rest_format_contributions(self):
        return [self.text]

    ### PUBLIC PROPERTIES ###

    @property
    def rest_format(self):
        r'''ReST format of ReST autosummary item.
        '''
        return '\n'.join(self._rest_format_contributions)

    @property
    def text(self):
        r'''Text of ReST autosummary item.
        '''
        return self._text

    @text.setter
    def text(self, arg):
        assert isinstance(arg, str)
        arg = arg.strip()
        assert len(arg)
        self._text = arg
