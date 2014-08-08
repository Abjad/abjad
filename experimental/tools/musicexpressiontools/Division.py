# -*- encoding: utf-8 -*-
from abjad.tools.mathtools.NonreducedFraction import NonreducedFraction


class Division(NonreducedFraction):
    r'''Division.

    A division is an optionally offset-positioned nonreduced fraction.

    ..  container:: example::
    
        Example 1. Initializes from pair:

        ::

            >>> musicexpressiontools.Division(5, 8)
            Division(5, 8)

    ..  container:: example::

        Example 2. Initializes from other division:

        ::

            >>> division = musicexpressiontools.Division(5, 8)
            >>> musicexpressiontools.Division(division)
            Division(5, 8)

    Divisions model beats, measures or any block of time divisible into parts.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_start_offset',
        )

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        result = type(self)(self.pair)
        if hasattr(self, '_start_offset'):
            result._start_offset = self._start_offset
        return result