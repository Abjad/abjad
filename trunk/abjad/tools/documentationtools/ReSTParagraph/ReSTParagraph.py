import textwrap
from abjad.tools.datastructuretools.TreeNode import TreeNode


class ReSTParagraph(TreeNode):
    '''An ReST paragraph:

    ::

        >>> paragraph = documentationtools.ReSTParagraph(text='blah blah blah')
        >>> paragraph
        ReSTParagraph(
            text='blah blah blah',
            wrap=True
            )

    ::

        >>> print _.rest_format
        blah blah blah

    Handles automatic linewrapping.

    Return `ReSTParagraph` instance.
    '''

    ### INITIALIZER ###

    def __init__(self, name=None, text='', wrap=True):
        TreeNode.__init__(self, name=name)
        self.text = text
        self.wrap = wrap

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _rest_format_contributions(self):
        if self.wrap:
            text = ' '.join(self.text.splitlines())
            return textwrap.wrap(text)
        return [self.text]

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def rest_format(self):
        return '\n'.join(self._rest_format_contributions)

    ### READ/WRITE PUBLIC PROPERTIES ###

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

    @apply
    def wrap():
        def fget(self):
            return self._wrap
        def fset(self, arg):
            self._wrap = bool(arg)
        return property(**locals())

