from experimental.quantizationtools.GraceHandler import GraceHandler


class DiscardingGraceHandler(GraceHandler):
    '''Discards all but final QEvent attached to an offset.

    Does not create GraceContainers.

    Return ``DiscardingGraceHandler`` instance.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, q_events):
        from experimental import quantizationtools

        q_event = q_events[-1]
        if isinstance(q_event, quantizationtools.PitchedQEvent):
            return q_event.pitches, None
        return (), None
