# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools.pitchtools.Vector import Vector


class IntervalVector(Vector):
    r'''Abjad model of an interval vector:

    ::

        >>> pitch_segment = pitchtools.PitchSegment(
        ...     tokens=[0, 11, 7, 4, 2, 9, 3, 8, 10, 1, 5, 6],
        ...     )
        >>> numbered_interval_vector = pitchtools.IntervalVector(
        ...     tokens=pitch_segment,
        ...     item_class=pitchtools.NumberedInterval,
        ...     )
        >>> for interval, count in numbered_interval_vector.iteritems():
        ...     print interval, count
        ...
        +4 4
        +5 3
        -8 2
        +3 5
        -5 4
        +2 5
        +1 5
        -4 4
        -6 3
        -7 3
        -11 1
        +8 2
        +9 2
        -10 1
        +7 2
        -1 6
        +6 3
        -9 1
        -2 5
        -3 4
        +10 1

    Return pitch segment.
    '''

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools
        if isinstance(tokens, (
            pitchtools.PitchSegment, 
            pitchtools.PitchSet,
            pitchtools.PitchClassSegment,
            pitchtools.PitchClassSet,
            )):
            intervals = []
            for first, second in \
                sequencetools.yield_all_unordered_pairs_of_sequence(
                    tuple(tokens)):
                intervals.append(second - first)
            tokens = intervals
        Vector.__init__(
            self,
            tokens=tokens,
            item_class=item_class,
            name=name,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedInterval
    
    @property
    def _numbered_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedInterval

    @property
    def _parent_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.Interval

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(cls, selection, item_class=None, name=None):
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        return cls(
            pitch_segment,
            item_class=item_class,
            name=name,
            )
