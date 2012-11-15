from abjad.tools.quantizationtools.GraceHandler import GraceHandler


class CollapsingGraceHandler(GraceHandler):
    '''A GraceHandler which collapses pitch information into a single Chord,
    rather than creating a GraceContainer.

    Return ``CollapsingGraceHandler`` instance.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, q_events):
        from abjad.tools import quantizationtools
        pitches = []
        for q_event in q_events:
            if isinstance(q_event, quantizationtools.PitchedQEvent):
                pitches.extend(q_event.pitches)
        return tuple(pitches), None
