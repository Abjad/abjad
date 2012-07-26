from abjad.tools import durationtools
from abjad.tools import notetools
from abjad.tools import rhythmtreetools
from experimental.quantizationtools.ProxyQEvent import ProxyQEvent


class QGridLeaf(rhythmtreetools.RhythmTreeNode):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_duration', '_offset', '_offsets_are_current', '_parent', '_q_events')

    ### INITIALIZER ###

    def __init__(self, duration=1, q_events=None):
        rhythmtreetools.RhythmTreeNode.__init__(self, duration)
        if q_events is None:
            q_events = []
        else:
            assert all([isinstance(x, ProxyQEvent) for x in q_events])
        self._q_events = list(q_events)

    ### SPECIAL METHODS ###

    def __call__(self, pulse_duration):
        pulse_duration = durationtools.Duration(pulse_duration)
        total_duration = pulse_duration * self.duration
        return notetools.make_notes(0, total_duration)


    def __deepcopy__(self, memo):
        return type(self)(*self.__getnewargs__())

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
    
