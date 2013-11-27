# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TreeNode import TreeNode


class ReSTHeading(TreeNode):
    r'''An ReST Heading:

    ::

        >>> heading = documentationtools.ReSTHeading(
        ...     level=2, text='Section A')
        >>> heading
        ReSTHeading(
            level=2,
            text='Section A'
            )

    ::

        >>> print heading.rest_format
        Section A
        =========

    Return `ReSTHeading` instance.
    '''

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
        return self._level

    @level.setter
    def level(self, arg):
        assert isinstance(arg, int) and \
            0 <= arg < len(self.heading_characters)
        self._level = arg

    @property
    def rest_format(self):
        return '\n'.join(self._rest_format_contributions)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, arg):
        assert isinstance(arg, str)
        arg = arg.strip()
        assert len(arg)
        self._text = arg
