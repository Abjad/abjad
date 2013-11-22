# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TreeNode import TreeNode


class ReSTTOCItem(TreeNode):
    r'''An ReST TOC item:

    ::

        >>> item = documentationtools.ReSTTOCItem(text='api/index')
        >>> item
        ReSTTOCItem(
            text='api/index'
            )

    ::

        >>> print item.rest_format
        api/index

    Return `ReSTTOCItem` instance.
    '''

    ### INITIALIZER ###

    def __init__(self, name=None, text=None):
        TreeNode.__init__(self, name)
        self.text = text

    ### PRIVATE PROPERTIES ###

    @property
    def _rest_format_contributions(self):
        return [self.text]

    ### PUBLIC PROPERTIES ###

    @property
    def rest_format(self):
        return '\n'.join(self._rest_format_contributions)

    ### PUBLIC PROPERTIES ###

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, arg):
        assert isinstance(arg, str)
        arg = arg.strip()
        assert len(arg)
        self._text = arg
