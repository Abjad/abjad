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
        ...     item_class=pitchtools.NumberedMelodicInterval,
        ...     )
        >>> for interval, count in numbered_interval_vector.iteritems():
        ...     print interval, count
        ...
        +8 2
        +9 2
        -4 4
        -2 5
        -3 4
        -1 6
        +3 5
        -10 1
        +5 3
        +10 1
        -9 1
        +7 2
        +2 5
        -11 1
        -8 2
        -6 3
        -7 3
        +6 3
        -5 4
        +1 5
        +4 4

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
        return pitchtools.NamedMelodicInterval
    
    @property
    def _numbered_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedMelodicInterval

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
