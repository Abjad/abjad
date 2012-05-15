from abc import ABCMeta
from abjad.tools.marktools.Mark import Mark
from abjad.tools.stringtools import arg_to_tridirectional_lilypond_symbol


class _DirectedMark(Mark):

    __metaclass__ = ABCMeta
    __slots__ = ('_direction', '_format_slot')

    def __init__(self, *args, **kwargs):
        Mark.__init__(self, *args)
        if 'direction' in kwargs:
            self.direction = kwargs['direction']
        else:
            self.direction = None
    
    ### PUBLIC PROPERTIES ###

    @apply
    def direction():
        def fget(self):
            return self._direction
        def fset(self, arg):
            self._direction = arg_to_tridirectional_lilypond_symbol(arg)
        return property(**locals())
