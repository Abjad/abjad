# -*- encoding: utf-8 -*-
import collections
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadValueObject


class DurationSelectorCallback(AbjadValueObject):
    r'''A duration selector callback.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_duration',
        '_parts',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        duration=durationtools.Duration(1, 4),
        parts=Exact,
        ):
        self._duration = durationtools.Duration(duration)
        if not isinstance(parts, collections.Sequence):
            parts = (parts,)
        assert all(_ in (None, Exact, More, Less) for _ in parts)
        self._parts = parts

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Iterates tuple `expr`.

        Returns tuple in which each item is a selection or component.
        '''
        from abjad.tools import scoretools
        assert isinstance(expr, tuple), repr(tuple)
        result = []
        for subexpr in expr:
            if isinstance(subexpr, scoretools.Component):
                duration = subexpr._get_duration()
            else:
                duration = subexpr.get_duration()
            if None in self.parts or Exact in self.parts:
                if duration == self.duration:
                    result.append(subexpr)
            elif More in self.parts:
                if self.duration < duration:
                    result.append(subexpr)
            elif Less in self.parts:
                if duration < self.duration:
                    result.append(subexpr)
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''Gets duration selector callback duration.

        Returns duration.
        '''
        return self._duration

    @property
    def parts(self):
        r'''Gets duration selector callback partial-result handling.

        Returns ordinal constant.
        '''
        return self._parts