from abjad.tools import chordtools
from abjad.tools import durationtools
from abjad.tools import gracetools
from abjad.tools import notetools
from abjad.tools import resttools
from experimental.quantizationtools.GraceHandler import GraceHandler
from experimental.quantizationtools.PitchedQEvent import PitchedQEvent


class ConcatenatingGraceHandler(GraceHandler):
    '''Concatenates all but final QEvent attached to an offset into a GraceContainer,
    using a fixed leaf duration `duration`.

    Returns pitch information of final QEvent, and the generated GraceContainer, if any.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_grace_duration',)

    ### INITIALIZER ###

    def __init__(self, grace_duration=None):
        if grace_duration is None:
            grace_duration = (1, 16)
        grace_duration = durationtools.Duration(grace_duration)
        assert durationtools.is_binary_rational(grace_duration)
        self._grace_duration = grace_duration

    ### SPECIAL METHODS ###

    def __call__(self, q_events):

        grace_events, final_event = q_events[:-1], q_events[-1]

        if isinstance(final_event, PitchedQEvent):
            pitches = final_event.pitches
        else:
            pitches = ()

        if grace_events:
            grace_container = gracetools.GraceContainer()
            for q_event in grace_events:
                if isinstance(q_event, PitchedQEvent):
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
