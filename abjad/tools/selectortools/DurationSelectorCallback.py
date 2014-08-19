# -*- encoding: utf-8 -*-
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
        assert parts in (None, Exact, More, Less)
        self._parts = parts

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Iterates `expr`.

        Returns tuple in which each item is a selection or component.
        '''
        from abjad.tools import scoretools
        result = []
        for subexpr in expr:
            if isinstance(subexpr, scoretools.Component):
                duration = subexpr._get_duration()
            else:
                duration = subexpr.get_duration()
            if self.parts in (None, Exact):
                if duration == self.duration:
                    result.append(subexpr)
            elif self.parts == More:
                if self.duration < duration:
                    result.append(subexpr)
            elif self.parts == Less:
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