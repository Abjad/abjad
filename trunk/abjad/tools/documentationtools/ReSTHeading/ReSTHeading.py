from abjad.tools.datastructuretools.TreeNode import TreeNode


class ReSTHeading(TreeNode):

    ### INITIALIZER ###

    def __init__(self, level=0, name=None, text=''):
        TreeNode.__init__(self, name=name)
        self.level = level
        self.text = text

    ### READ/WRITE PUBLIC PROPERTIES ###

    @apply
    def level():
        def fget(self):
            return self._level
        def fset(self, arg):
            assert isinstance(arg, int) and 0 < arg
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

