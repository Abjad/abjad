# -*- coding: utf-8 -*-
from abjad.tools.quantizationtools.GraceHandler import GraceHandler


class DiscardingGraceHandler(GraceHandler):
    r'''Concrete ``GraceHandler`` subclass which discards all but final
    ``QEvent`` attached to an offset.

    Does not create ``GraceContainers``.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, q_events):
        r'''Calls idscarind grace handler.
        '''
        from abjad.tools import quantizationtools
        q_event = q_events[-1]
        if isinstance(q_event, quantizationtools.PitchedQEvent):
            return q_event.pitches, None
        return (), None
