from abjad.tools import durationtools
from abjad.tools import notetools
from abjad.tools import rhythmtreetools
from experimental.quantizationtools.QEventProxy import QEventProxy


class QGridLeaf(rhythmtreetools.RhythmTreeNode):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_duration', '_is_divisible', '_offset', '_offsets_are_current',
        '_parent', '_q_events')

    ### INITIALIZER ###

    def __init__(self, duration=1, q_events=None, is_divisible=True):
        rhythmtreetools.RhythmTreeNode.__init__(self, duration)
        if q_events is None:
            q_events = []
        else:
            assert all([isinstance(x, QEventProxy) for x in q_events])
        self._q_events = list(q_events)
        self._is_divisible = bool(is_divisible)

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
                    if self._is_divisible == other.is_divisible:
                        return True
        return False

    def __getnewargs__(self):
        return (self.duration, tuple(self.q_events), self.is_divisible)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def rtm_format(self):
        return str(self.duration)

    @property
    def q_events(self):
        return self._q_events
    
    ### READ/WRITE PUBLIC PROPERTIES ###

    @apply
    def is_divisible():
        def fget(self):
            '''Flag for whether the node may be further divided under some search tree.'''
            return self._is_divisible
        def fset(self, arg):
            self._is_divisible = bool(arg)
        return property(**locals())
