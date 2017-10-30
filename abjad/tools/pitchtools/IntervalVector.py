from abjad.tools import mathtools
from abjad.tools.pitchtools.Vector import Vector


class IntervalVector(Vector):
    r'''Interval vector.

    ..  container:: example

        Initializes from pitch segment:

        >>> pitch_segment = abjad.PitchSegment(
        ...     items=[0, 11, 7, 4, 2, 9, 3, 8, 10, 1, 5, 6],
        ...     )
        >>> numbered_interval_vector = abjad.IntervalVector(
        ...     items=pitch_segment,
        ...     item_class=abjad.NumberedInterval,
        ...     )
        >>> for interval, count in sorted(numbered_interval_vector.items(),
        ...     key=lambda x: (x[0].direction_number, x[0].number)):
        ...     print(interval, count)
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

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        from abjad.tools import pitchtools
        if isinstance(items, (
            pitchtools.PitchSegment,
            pitchtools.PitchSet,
            pitchtools.PitchClassSegment,
            pitchtools.PitchClassSet,
            )):
            intervals = []
            enumerator = mathtools.Enumerator(items)
            pairs = enumerator.yield_pairs()
            for first, second in pairs:
                intervals.append(second - first)
            items = intervals
        Vector.__init__(
            self,
            items=items,
            item_class=item_class,
            )

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpret representation of interval vector.

        ..  container:: example

            Gets interpreter representation of interval vector:

            >>> pitch_segment = abjad.PitchSegment(
            ...     items=[0, 11, 7, 4, 2, 9, 3, 8, 10, 1, 5, 6],
            ...     )
            >>> vector = abjad.IntervalVector(
            ...     items=pitch_segment,
            ...     item_class=abjad.NumberedInterval,
            ...     )

            >>> vector
            IntervalVector({-11: 1, -10: 1, -9: 1, -8: 2, -7: 3, -6: 3, -5: 4, -4: 4, -3: 4, -2: 5, -1: 6, 1: 5, 2: 5, 3: 5, 4: 4, 5: 3, 6: 3, 7: 2, 8: 2, 9: 2, 10: 1}, item_class=NumberedInterval)

        ..  container:: example

            Initializes from interpreter representation of interval vector:

            >>> abjad.IntervalVector(vector)
            IntervalVector({-11: 1, -10: 1, -9: 1, -8: 2, -7: 3, -6: 3, -5: 4, -4: 4, -3: 4, -2: 5, -1: 6, 1: 5, 2: 5, 3: 5, 4: 4, 5: 3, 6: 3, 7: 2, 8: 2, 9: 2, 10: 1}, item_class=NumberedInterval)

        Returns string.
        '''
        superclass = super(IntervalVector, self)
        return superclass.__repr__()

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
        class_,
        selection,
        item_class=None,
        ):
        r'''Makes interval vector from `selection`.

        Returns interval vector.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        return class_(
            pitch_segment,
            item_class=item_class,
            )
