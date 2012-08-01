from experimental.quantizationtools.GraceHandler import GraceHandler
from experimental.quantizationtools.PitchedQEvent import PitchedQEvent


class DiscardingGraceHandler(GraceHandler):
    '''Discards all but final QEvent attached to an offset.

    Does not create GraceContainers.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, q_events):

        q_event = q_events[-1]
        if isinstance(q_event, PitchedQEvent):
            return q_event.pitches, None
        return (), None
