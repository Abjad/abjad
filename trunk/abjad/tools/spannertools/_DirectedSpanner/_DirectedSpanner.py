from abc import ABCMeta
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools import stringtools


class _DirectedSpanner(Spanner):
    
    __metaclass__ = ABCMeta

    def __init__(self, components=[], direction=None):
        Spanner.__init__(self, components)
        self.direction = direction

    ### PUBLIC PROPERTIES ###

    @apply
    def direction():
        def fget(self):
            return self._direction
        def fset(self, arg):
            self._direction = stringtools.arg_to_tridirectional_ordinal_constant(arg)
        return property(**locals())
