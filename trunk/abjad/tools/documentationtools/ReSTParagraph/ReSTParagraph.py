import textwrap
from abjad.tools.datastructuretools.TreeNode import TreeNode


class ReSTParagraph(TreeNode):
    '''An ReST paragraph:

    ::

        >>> paragraph = documentationtools.ReSTParagraph(text='blah blah blah')
        >>> paragraph
        ReSTParagraph(
            text='blah blah blah'
            )

    ::

        >>> print _.rest_format
        blah blah blah

    Handles automatic linewrapping.

    Return `ReSTParagraph` instance.
    ''' 

    ### INITIALIZER ###

    def __init__(self, name=None, text=''):
        TreeNode.__init__(self, name=name)
        self.text = text

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _rest_format_contributions(self):
        text = ' '.join(self.text.split('\n'))
        return textwrap.wrap(text)

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

