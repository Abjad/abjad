from abjad.tools.quantizationtools.GraceHandler import GraceHandler


class DiscardingGraceHandler(GraceHandler):
    '''Concrete ``GraceHandler`` subclass which discards all but final
    ``QEvent`` attached to an offset.

    Does not create ``GraceContainers``.

    Return ``DiscardingGraceHandler`` instance.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, q_events):
        from abjad.tools import quantizationtools

        q_event = q_events[-1]
        if isinstance(q_event, quantizationtools.PitchedQEvent):
            return q_event.pitches, None
        return (), None
