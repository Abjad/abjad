from abjad.tools.datastructuretools.TreeNode import TreeNode


class ReSTParagraph(TreeNode):

    ### INITIALIZER ###

    def __init__(self, name=None, text=''):
        TreeNode.__init__(self, name=name)
        self.text = text

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

