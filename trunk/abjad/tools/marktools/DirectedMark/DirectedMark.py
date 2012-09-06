import abc
from abjad.tools import stringtools
from abjad.tools.marktools.Mark import Mark


class DirectedMark(Mark):
    '''Abstract base class of Marks which possess a vertical, typographic direction, 
    i.e. above or below the staff.
    '''    

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_direction', '_format_slot')

    ### INITIALIZER ###

    @abc.abstractmethod
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
            self._direction = stringtools.arg_to_tridirectional_ordinal_constant(arg)
        return property(**locals())
