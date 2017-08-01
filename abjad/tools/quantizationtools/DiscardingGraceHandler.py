# -*- coding: utf-8 -*-
from abjad.tools.quantizationtools.GraceHandler import GraceHandler


class DiscardingGraceHandler(GraceHandler):
    r'''Discarindg grace-handler.
    
    Dscards all but final q-event attached to an offset.

    ::

        >>> import abjad
        >>> from abjad.tools import quantizationtools

    Does not create grace containers.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __call__(self, q_events):
        r'''Calls idscarind grace handler.
        '''
        from abjad.tools import quantizationtools
        q_event = q_events[-1]
        if isinstance(q_event, quantizationtools.PitchedQEvent):
            return q_event.pitches, None
        return (), None
