from abjad.tools.documentationtools.ReSTDirective import ReSTDirective


class ReSTOnlyDirective(ReSTDirective):
    
    ### INITIALIZER ###

    def __init__(self, children=None, name=None, expr=None):
        ReSTDirective.__init__(self, children=children, name=name)
        self.expr = expr

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def directive(self):
        return 'only'

    ### READ/WRITE PUBLIC PROPERTIES ###

    @apply
    def expr():
        def fget(self):
            return self._expr
        def fset(self, arg):
            assert isinstance(arg, str)
            arg = arg.strip()
            assert len(arg)
            self._expr = arg
        return property(**locals())

