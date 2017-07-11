# -*- coding: utf-8 -*-
import collections
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadValueObject


class DurationSelectorCallback(AbjadValueObject):
    r'''Duration selector callback.

    ::

        >>> import abjad

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
        if not isinstance(duration, prototype):
            duration = durationtools.Duration(duration)
        self._duration = duration
        if preprolated is not None:
            preprolated = bool(preprolated)
        self._preprolated = preprolated

    ### SPECIAL METHODS ###

    def __call__(self, argument, rotation=None):
        r'''Iterates tuple `argument`.

        Returns tuple in which each item is a selection or component.
        '''
        from abjad.tools import scoretools
        from abjad.tools import selectortools
        assert isinstance(argument, collections.Iterable), repr(argument)
        inequality = self.duration
        if not isinstance(inequality, selectortools.DurationInequality):
            inequality = selectortools.DurationInequality(
                duration=inequality,
                operator_string='==',
                )
        result = []
        for subexpr in argument:
            if not self.preprolated:
                if isinstance(subexpr, scoretools.Component):
                    duration = subexpr._get_duration()
                else:
                    duration = subexpr.get_duration()
            else:
                if isinstance(subexpr, scoretools.Component):
                    subexpr._update_now(offsets=True)
                    duration = subexpr._get_preprolated_duration()
                else:
                    durations = []
                    for x in subexpr:
                        if isinstance(x, scoretools.Component):
                            x._update_now(offsets=True)
                        duration = x._get_preprolated_duration()
                        durations.append(x._get_preprolated_duration())
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
