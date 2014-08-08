# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import timespantools
from abjad.tools.mathtools.NonreducedFraction import NonreducedFraction


class Division(NonreducedFraction):
    r'''Division.

    A division is a nonreduced fraction that is optionally
    offset-positioned.

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

    Divisions model any block of time that is divisible into parts: beats,
    complete measures, etc.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_start_offset',
        )

    ### CONSTRUCTOR ###

    def __new__(
        cls,
        *args,
        **kwargs
        ):
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, str):
                raise Exception(str)
            elif isinstance(arg, cls):
                pair = arg
            elif hasattr(arg, 'duration'):
                pair = (arg.duration.numerator, arg.duration.denominator)
            else:
                pair = arg
        elif len(args) == 2:
            pair = args
        else:
            raise ValueError(args)
        self = NonreducedFraction.__new__(cls, pair)

        # TODO: remove
        start_offset = kwargs.get('start_offset')
        if start_offset is None:
            start_offset = getattr(pair, 'start_offset', None)
        self._start_offset = start_offset

        return self

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return type(self)(
            self.pair,
            start_offset=self._start_offset,
            )