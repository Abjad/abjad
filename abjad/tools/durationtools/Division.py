# -*- encoding: utf-8 -*-
from abjad.tools.mathtools.NonreducedFraction import NonreducedFraction


class Division(NonreducedFraction):
    r'''Division.

    A division is a nonreduced fraction used to model beats, measures
    or any block of time divisible into parts.

    ..  container:: example::
    
        Example 1. Initializes from pair:

        ::

            >>> division = durationtools.Division(5, 8)
            >>> division
            Division(5, 8)

    ..  container:: example::

        Example 2. Initializes from other division:

        ::

            >>> durationtools.Division(division)
            Division(5, 8)

    Divisions are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )