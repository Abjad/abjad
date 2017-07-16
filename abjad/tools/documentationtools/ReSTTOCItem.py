# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools.datastructuretools.TreeNode import TreeNode


class ReSTTOCItem(TreeNode):
    r'''A ReST TOC item.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> item = abjad.documentationtools.ReSTTOCItem(text='api/index')
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

    __slots__ = (
        '_text',
        )

    ### INITIALIZER ###

    def __init__(self, name=None, text='foo'):
        TreeNode.__init__(self, name)
        #self.text = text
        self._text = text

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
        assert datastructuretools.String.is_string(arg)
        arg = arg.strip()
        self._text = arg
