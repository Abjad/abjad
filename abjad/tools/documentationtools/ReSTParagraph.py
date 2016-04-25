# -*- coding: utf-8 -*-
import textwrap
from abjad.tools.datastructuretools.TreeNode import TreeNode


class ReSTParagraph(TreeNode):
    r'''A ReST paragraph.

    ::

        >>> paragraph = documentationtools.ReSTParagraph(
        ...     text='blah blah blah')
        >>> paragraph
        ReSTParagraph(
            text='blah blah blah',
            wrap=True
            )

    ::

        >>> print(_.rest_format)
        blah blah blah

    Handles automatic linewrapping.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'reStructuredText'

    ### INITIALIZER ###

    def __init__(self, name=None, text='foo', wrap=True):
        TreeNode.__init__(self, name=name)
        self.text = text
        self.wrap = wrap

    ### PRIVATE PROPERTIES ###

    @property
    def _rest_format_contributions(self):
        if self.wrap:
            text = ' '.join(self.text.splitlines())
            return textwrap.wrap(text)
        return [self.text]

    ### PUBLIC PROPERTIES ###

    @property
    def rest_format(self):
        r'''ReST format of ReST paragraph.

        Returns string.
        '''
        return '\n'.join(self._rest_format_contributions)

    @property
    def text(self):
        r'''Gets and sets text of ReST paragraph.

        Returns string.
        '''
        return self._text

    @text.setter
    def text(self, arg):
        assert isinstance(arg, str)
        arg = arg.strip()
        assert len(arg)
        self._text = arg

    @property
    def wrap(self):
        r'''Gets and sets wrap flag of ReST paragraph.

        Returns true or false.
        '''
        return self._wrap

    @wrap.setter
    def wrap(self, arg):
        self._wrap = bool(arg)
