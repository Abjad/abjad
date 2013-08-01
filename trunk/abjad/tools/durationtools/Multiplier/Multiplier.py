# -*- encoding: utf-8 -*-
from abjad.tools import abctools
from abjad.tools import mathtools
from abjad.tools.durationtools.Duration import Duration


class Multiplier(Duration):
    '''Multiplier.
    '''

    ### SPECIAL METHODS ###

    def __mul__(self, *args):
        r'''Multiplier times duration gives duration.

        Return duration.
        '''
        if len(args) == 1 and type(args[0]) is Duration:
            return Duration(Duration.__mul__(self, *args))
        else:
            return Duration.__mul__(self, *args)

    ### PUBLIC PROPERTIES ###

    @property
    def is_proper_tuplet_multiplier(self):
        '''.. versionadded:: 2.11

        True when mutliplier is greater than ``1/2`` and less than ``2``.
        Otherwise false:

        ::

            >>> Multiplier(3, 2).is_proper_tuplet_multiplier
            True

        Return boolean.
        '''
        return type(self)(1, 2) < self < type(self)(2)
