from abjad.tools import durationtools
from abjad.tools import notetools
from abjad.tools.rhythmtreetools import RhythmTreeNode


class QGridLeaf(RhythmTreeNode):
    '''A leaf in a ``QGrid`` structure:

    ::

        >>> leaf = quantizationtools.QGridLeaf()

    ::

        >>> leaf
        quantizationtools.QGridLeaf(
            duration=durationtools.Duration(1, 1),
            q_event_proxies=[],
            is_divisible=True
            )

    Used internally by ``QGrid``.

    Return ``QGridLeaf`` instance.
    '''

    ### CLASS ATTRIBUTES ###

    #__slots__ = ('_duration', '_is_divisible', '_offset', '_offsets_are_current',
    #    '_parent', '_q_event_proxies')

    ### INITIALIZER ###

    def __init__(self, duration=1, q_event_proxies=None, is_divisible=True):
        from abjad.tools import quantizationtools
        RhythmTreeNode.__init__(self, duration)
        if q_event_proxies is None:
            self._q_event_proxies = []
        else:
            assert all([isinstance(x, quantizationtools.QEventProxy) for x in q_event_proxies])
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

    def __repr__(self):
        return self._tools_package_qualified_indented_repr

    ### READ-ONLY PRIVATE PROPERTIES ###
        
    @property
    def _pretty_rtm_format_pieces(self):
        return [str(self.duration)]

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def rtm_format(self):
        return str(self.duration)

    @property
    def preceding_q_event_proxies(self):
        return [x for x in self._q_event_proxies if x.offset < self.start_offset]

    @property
    def q_event_proxies(self):
        return self._q_event_proxies

    @property
    def succeeding_q_event_proxies(self):
        return [x for x in self._q_event_proxies if self.start_offset <= x.offset]

    ### READ/WRITE PUBLIC PROPERTIES ###

    @apply
    def is_divisible():
        def fget(self):
            '''Flag for whether the node may be further divided under some search tree.'''
            return self._is_divisible
        def fset(self, arg):
            self._is_divisible = bool(arg)
        return property(**locals())
