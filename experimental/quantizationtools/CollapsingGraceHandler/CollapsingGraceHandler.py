from experimental.quantizationtools.GraceHandler import GraceHandler
from experimental.quantizationtools.PitchedQEvent import PitchedQEvent


class CollapsingGraceHandler(GraceHandler):
    '''Collapses pitch information into chords.

    Does not create GraceContainers.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, q_events):
        pitches = []
        for q_event in q_events:
            if isinstance(q_event, PitchedQEvent):
                pitches.extend(q_event.pitches)
        return tuple(pitches), None
