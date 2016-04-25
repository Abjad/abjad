# -*- coding: utf-8 -*-
from abjad.tools.quantizationtools.GraceHandler import GraceHandler


class CollapsingGraceHandler(GraceHandler):
    r'''A GraceHandler which collapses pitch information into a single chord
    rather than creating a grace container.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, q_events):
        r'''Calls collapsing grace handler.
        '''
        from abjad.tools import quantizationtools
        pitches = []
        for q_event in q_events:
            if isinstance(q_event, quantizationtools.PitchedQEvent):
                pitches.extend(q_event.pitches)
        return tuple(pitches), None
