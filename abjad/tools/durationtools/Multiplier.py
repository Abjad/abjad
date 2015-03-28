# -*- encoding: utf-8 -*-
from abjad.tools.durationtools.Duration import Duration


class Multiplier(Duration):
    '''A multiplier.

    ::

        >>> Multiplier(2, 3)
        Multiplier(2, 3)

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __mul__(self, *args):
        r'''Multiplier times duration gives duration.

        Returns duration.
        '''
        if len(args) == 1 and type(args[0]) is Duration:
            return Duration(Duration.__mul__(self, *args))
        else:
            return Duration.__mul__(self, *args)

    ### PUBLIC PROPERTIES ###

    @property
    def is_proper_tuplet_multiplier(self):
        '''Is true when mutliplier is greater than ``1/2`` and less than ``2``.
        Otherwise false:

        ::

            >>> Multiplier(3, 2).is_proper_tuplet_multiplier
            True

        Returns boolean.
        '''
        return type(self)(1, 2) < self < type(self)(2)