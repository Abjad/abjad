from abjad.tools import rhythmtreetools
from experimental.quantizationtools.QEvent import QEvent


class QGridLeaf(rhythmtreetools.RhythmTreeNode):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_duration', '_offset', '_offsets_are_current', '_parent', '_q_events')

    ### INITIALIZER ###

    def __init__(self, duration=1, q_events=None):
        rhythmtreetools.RhythmTreeNode.__init__(self, duration)
        if q_events is None:
            q_events = ()
        else:
            assert all([isinstance(x, QEvent) for x in q_events])
        self._q_events = q_events

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        if type(self) == type(other):
            if self.duration == other.duration:
                if self.q_events == other.q_events:
                    return True
        return False

    def __getnewargs__(self):
        return (self.duration, tuple(self.q_events))

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def rtm_format(self):
        return str(self.duration)

    @property
    def q_events(self):
        return self._q_events
    
