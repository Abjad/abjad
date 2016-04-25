# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools.TreeNode import TreeNode


class ReSTHeading(TreeNode):
    r'''A ReST heading.

    ::

        >>> heading = documentationtools.ReSTHeading(
        ...     level=2, text='Section A')
        >>> heading
        ReSTHeading(
            level=2,
            text='Section A'
            )

    ::

        >>> print(heading.rest_format)
        Section A
        =========

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'reStructuredText'

    ### INITIALIZER ###

    def __init__(self, level=0, name=None, text='foo'):
        TreeNode.__init__(self, name=name)
        self.level = level
        self.text = text

    ### PRIVATE PROPERTIES ###

    @property
    def _rest_format_contributions(self):
        result = []
        underline, overline = self.heading_characters[self.level]
        if overline:
            result.append(overline * len(self.text))
        result.append(self.text)
        result.append(underline * len(self.text))
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def heading_characters(self):
        r'''Heading characters of ReST heading.
        '''
        return (
            ('#', '#'),
            ('*', '*'),
            ('=', None),
            ('-', None),
            ('^', None),
            ('"', None),
        )

    @property
    def level(self):
        r'''Gets and sets level of ReST heading.
        '''
        return self._level

    @level.setter
    def level(self, arg):
        assert isinstance(arg, int) and \
            0 <= arg < len(self.heading_characters)
        self._level = arg

    @property
    def rest_format(self):
        r'''ReST format of ReST heading.

        Returns string.
        '''
        return '\n'.join(self._rest_format_contributions)

    @property
    def text(self):
        r'''Gets and sets text of ReST heading.

        Returns string.
        '''
        return self._text

    @text.setter
    def text(self, arg):
        assert isinstance(arg, str)
        arg = arg.strip()
        assert len(arg)
        self._text = arg
