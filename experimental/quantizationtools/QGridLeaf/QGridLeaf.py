from abjad.tools import rhythmtreetools


class QGridLeaf(rhythmtreetools.RhythmTreeLeaf):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_duration', '_parent', '_q_events')

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def q_events(self):
        return self.q_events
    
