from abjad.tools.datastructuretools.TreeNode import TreeNode


class ReSTHeading(TreeNode):
    '''An ReST Heading:

    ::

        >>> heading = documentationtools.ReSTHeading(level=2, text='Section A')
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

    def __init__(self, level=0, name=None, text=''):
        TreeNode.__init__(self, name=name)
        self.level = level
        self.text = text

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _rest_format_contributions(self):
        result = []
        underline, overline = self.heading_characters[self.level] 
        if overline:
            result.append(overline * len(self.text))
        result.append(self.text)
        result.append(underline * len(self.text))
        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

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
    def rest_format(self):
        return '\n'.join(self._rest_format_contributions)

    ### READ/WRITE PUBLIC PROPERTIES ###

    @apply
    def level():
        def fget(self):
            return self._level
        def fset(self, arg):
            assert isinstance(arg, int) and \
                0 <= arg < len(self.heading_characters)
            self._level = arg
        return property(**locals())

    @apply
    def text():
        def fget(self):
            return self._text
        def fset(self, arg):
            assert isinstance(arg, str)
            arg = arg.strip()
            assert len(arg)
            self._text = arg
        return property(**locals())

