from abjad.tools.datastructuretools.TreeNode import TreeNode


class ReSTTOCItem(TreeNode):
    '''An ReST TOC item:

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

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _rest_format_contributions(self):
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

