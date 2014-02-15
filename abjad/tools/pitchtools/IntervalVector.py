# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools.pitchtools.Vector import Vector


class IntervalVector(Vector):
    r'''An interval vector.

    ::

        >>> pitch_segment = pitchtools.PitchSegment(
        ...     tokens=[0, 11, 7, 4, 2, 9, 3, 8, 10, 1, 5, 6],
        ...     )
        >>> numbered_interval_vector = pitchtools.IntervalVector(
        ...     tokens=pitch_segment,
        ...     item_class=pitchtools.NumberedInterval,
        ...     )
        >>> for interval, count in sorted(numbered_interval_vector.items(),
        ...     key=lambda x: (x[0].direction_number, x[0].number)):
        ...     print interval, count
        ...
        -11 1
        -10 1
        -9 1
        -8 2
        -7 3
        -6 3
        -5 4
        -4 4
        -3 4
        -2 5
        -1 6
        +1 5
        +2 5
        +3 5
        +4 4
        +5 3
        +6 3
        +7 2
        +8 2
        +9 2
        +10 1

    '''

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None):
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
    def from_selection(
        cls, 
        selection, 
        item_class=None, 
        ):
        r'''Makes interval vector from `selection`.

        Returns interval vector.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        return cls(
            pitch_segment,
            item_class=item_class,
            )
