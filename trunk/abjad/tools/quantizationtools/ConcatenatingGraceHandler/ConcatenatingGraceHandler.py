from abjad.tools import chordtools
from abjad.tools import durationtools
from abjad.tools import gracetools
from abjad.tools import notetools
from abjad.tools import resttools
from experimental.quantizationtools.GraceHandler import GraceHandler


class ConcatenatingGraceHandler(GraceHandler):
    '''Concrete ``GraceHandler`` subclass which concatenates all but the 
    final ``QEvent`` attached to a ``QGrid`` offset into a ``GraceContainer``,
    using a fixed leaf duration ``duration``.

    When called, it returns pitch information of final ``QEvent``, and the
    generated ``GraceContainer``, if any.

    Return ``ConcatenatingGraceHandler`` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_grace_duration',)

    ### INITIALIZER ###

    def __init__(self, grace_duration=None):
        if grace_duration is None:
            grace_duration = (1, 16)
        grace_duration = durationtools.Duration(grace_duration)
        assert grace_duration.has_power_of_two_denominator
        self._grace_duration = grace_duration

    ### SPECIAL METHODS ###

    def __call__(self, q_events):
        from experimental import quantizationtools

        grace_events, final_event = q_events[:-1], q_events[-1]

        if isinstance(final_event, quantizationtools.PitchedQEvent):
            pitches = final_event.pitches
        else:
            pitches = ()

        if grace_events:
            grace_container = gracetools.GraceContainer()
            for q_event in grace_events:
                if isinstance(q_event, quantizationtools.PitchedQEvent):
                    if len(q_event.pitches) == 1:
                        leaf = notetools.Note(q_event.pitches[0], self.grace_duration)
                    else:
                        leaf = chordtools.Chord(q_event.pitches, self.grace_duration)
                else:
                    leaf = resttools.Rest(self.grace_duration)
                grace_container.append(leaf)
        else:
            grace_container = None

        return pitches, grace_container

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def grace_duration(self):
        return self._grace_duration
