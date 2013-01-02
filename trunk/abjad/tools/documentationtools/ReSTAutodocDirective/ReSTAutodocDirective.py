from abjad.tools.documentationtools.ReSTDirective import ReSTDirective


class ReSTAutodocDirective(ReSTDirective):

    ### INITIALIZER ###

    def __init__(self, children=None, directive=None, name=None, options=None):
        ReSTDirective.__init__(self, children=children, name=name, options=options)
        self.directive = directive

    ### READ/WRITE PUBLIC PROPERTIES ###

    @apply
    def directive():
        def fget(self):
            return self.directive
        def fset(self, arg):
            assert arg in (
                'autoattribute',
                'autoclass',
                'autodata',
                'autoexception',
                'autofunction',
                'automethod',
                'automodule',
            )
            self._directive = arg
        return property(**locals())
