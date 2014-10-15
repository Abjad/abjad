# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadValueObject


class DurationSelectorCallback(AbjadValueObject):
    r'''A duration selector callback.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_duration',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        duration=durationtools.Duration(1, 4),
        ):
        from abjad.tools import selectortools
        prototype = (
            durationtools.Duration,
            selectortools.DurationInequality,
            )
        assert isinstance(duration, prototype)
        self._duration = duration

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Iterates tuple `expr`.

        Returns tuple in which each item is a selection or component.
        '''
        from abjad.tools import scoretools
        from abjad.tools import selectortools
        assert isinstance(expr, tuple), repr(tuple)
        inequality = self.duration
        if not isinstance(inequality, selectortools.DurationInequality):
            inequality = selectortools.DurationInequality(
                duration=inequality,
                operator_string='==',
                )
        result = []
        for subexpr in expr:
            if isinstance(subexpr, scoretools.Component):
                duration = subexpr._get_duration()
            else:
                duration = subexpr.get_duration()
            if inequality(duration):
                result.append(subexpr)
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''Gets duration selector callback duration.

        Returns duration or duration inequality.
        '''
        return self._duration