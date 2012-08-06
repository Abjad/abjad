from abjad.tools import durationtools
from abjad.tools import notetools
from abjad.tools import rhythmtreetools
from experimental.quantizationtools.QEventProxy import QEventProxy


class QGridLeaf(rhythmtreetools.RhythmTreeNode):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_duration', '_is_divisible', '_offset', '_offsets_are_current',
        '_parent', '_q_event_proxies')

    ### INITIALIZER ###

    def __init__(self, duration=1, q_event_proxies=None, is_divisible=True):
        rhythmtreetools.RhythmTreeNode.__init__(self, duration)
        if q_event_proxies is None:
            self._q_event_proxies = []
        else:
            assert all([isinstance(x, QEventProxy) for x in q_event_proxies])
            self._q_event_proxies = list(q_event_proxies)            
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
                if self.q_event_proxies == other.q_event_proxies:
                    if self._is_divisible == other.is_divisible:
                        return True
        return False

    def __getnewargs__(self):
       return (self.duration, tuple(self.q_event_proxies), self.is_divisible)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def rtm_format(self):
        return str(self.duration)

    @property
    def preceding_q_event_proxies(self):
        return [x for x in self._q_event_proxies if x.offset < self.offset]

    @property
    def q_event_proxies(self):
        return self._q_event_proxies

    @property
    def succeeding_q_event_proxies(self):
        return [x for x in self._q_event_proxies if self.offset <= x.offset]

    ### READ/WRITE PUBLIC PROPERTIES ###

    @apply
    def is_divisible():
        def fget(self):
            '''Flag for whether the node may be further divided under some search tree.'''
            return self._is_divisible
        def fset(self, arg):
            self._is_divisible = bool(arg)
        return property(**locals())
