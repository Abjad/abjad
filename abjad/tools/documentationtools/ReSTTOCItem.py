# -*- coding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.datastructuretools.TreeNode import TreeNode


class ReSTTOCItem(TreeNode):
    r'''A ReST TOC item.

    ::

        >>> item = documentationtools.ReSTTOCItem(text='api/index')
        >>> item
        ReSTTOCItem(
            text='api/index'
            )

    ::

        >>> print(item.rest_format)
        api/index

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
        r'''ReST format of ReST TOC item.

        Returns string.
        '''
        return '\n'.join(self._rest_format_contributions)

    @property
    def text(self):
        r'''Gets and sets text of ReST TOC item.

        Returns string.
        '''
        return self._text

    @text.setter
    def text(self, arg):
        assert stringtools.is_string(arg)
        arg = arg.strip()
        self._text = arg
