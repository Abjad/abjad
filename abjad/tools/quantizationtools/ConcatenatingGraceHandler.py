# -*- coding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools.quantizationtools.GraceHandler import GraceHandler


class ConcatenatingGraceHandler(GraceHandler):
    r'''Concrete ``GraceHandler`` subclass which concatenates all but the
    final ``QEvent`` attached to a ``QGrid`` offset into a ``GraceContainer``,
    using a fixed leaf duration ``duration``.

    When called, it returns pitch information of final ``QEvent``, and the
    generated ``GraceContainer``, if any.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_grace_duration',
        )

    ### INITIALIZER ###

    def __init__(self, grace_duration=None):
        if grace_duration is None:
            grace_duration = (1, 16)
        grace_duration = durationtools.Duration(grace_duration)
        assert grace_duration.has_power_of_two_denominator
        self._grace_duration = grace_duration

    ### SPECIAL METHODS ###

    def __call__(self, q_events):
        r'''Calls concatenating grace handler.
        '''
        from abjad.tools import quantizationtools

        grace_events, final_event = q_events[:-1], q_events[-1]

        if isinstance(final_event, quantizationtools.PitchedQEvent):
            pitches = final_event.pitches
        else:
            pitches = ()

        if grace_events:
            grace_container = scoretools.GraceContainer()
            for q_event in grace_events:
                if isinstance(q_event, quantizationtools.PitchedQEvent):
                    if len(q_event.pitches) == 1:
                        leaf = scoretools.Note(
                            q_event.pitches[0], self.grace_duration)
                    else:
                        leaf = scoretools.Chord(
                            q_event.pitches, self.grace_duration)
                else:
                    leaf = scoretools.Rest(self.grace_duration)
                grace_container.append(leaf)
        else:
            grace_container = None

        return pitches, grace_container

    ### PUBLIC PROPERTIES ###

    @property
    def grace_duration(self):
        r'''Grace duration of concantenating grace handler.

        Returns duration.
        '''
        return self._grace_duration
