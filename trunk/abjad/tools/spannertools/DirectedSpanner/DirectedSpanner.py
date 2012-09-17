import abc
from abjad.tools import stringtools
from abjad.tools.spannertools.Spanner import Spanner


class DirectedSpanner(Spanner):
    
    @abc.abstractmethod
    def __init__(self, components=[], direction=None):
        Spanner.__init__(self, components)
        self.direction = direction

    ### PUBLIC PROPERTIES ###

    @apply
    def direction():
        def fget(self):
            return self._direction
        def fset(self, arg):
            self._direction = stringtools.arg_to_tridirectional_lilypond_symbol(arg)
        return property(**locals())

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _copy_keyword_args(self, new):
        new.direction = self.direction

