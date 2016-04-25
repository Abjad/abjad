# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadValueObject


class DurationSelectorCallback(AbjadValueObject):
    r'''A duration selector callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_duration',
        '_preprolated',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        duration=durationtools.Duration(1, 4),
        preprolated=None,
        ):
        from abjad.tools import selectortools
        prototype = (
            durationtools.Duration,
            selectortools.DurationInequality,
            )
        assert isinstance(duration, prototype)
        self._duration = duration
        if preprolated is not None:
            preprolated = bool(preprolated)
        self._preprolated = preprolated

    ### SPECIAL METHODS ###

    def __call__(self, expr, rotation=None):
        r'''Iterates tuple `expr`.

        Returns tuple in which each item is a selection or component.
        '''
        from abjad.tools import scoretools
        from abjad.tools import selectortools
        assert isinstance(expr, tuple), repr(expr)
        inequality = self.duration
        if not isinstance(inequality, selectortools.DurationInequality):
            inequality = selectortools.DurationInequality(
                duration=inequality,
                operator_string='==',
                )
        result = []
        for subexpr in expr:
            if not self.preprolated:
                if isinstance(subexpr, scoretools.Component):
                    duration = subexpr._get_duration()
                else:
                    duration = subexpr.get_duration()
            else:
                if isinstance(subexpr, scoretools.Component):
                    subexpr._update_now(offsets=True)
                    duration = subexpr._preprolated_duration
                else:
                    durations = []
                    for x in subexpr:
                        if isinstance(x, scoretools.Component):
                            x._update_now(offsets=True)
                        duration = x._preprolated_duration
                        durations.append(x._preprolated_duration)
                    duration = sum(durations)
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

    @property
    def preprolated(self):
        r'''Is true if duration selector callback should be tested against the
        preprolated duration of components in selections. Otherwise false.

        Returns boolean or none.
        '''
        return self._preprolated
