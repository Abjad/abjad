# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools.pitchtools.Vector import Vector


class IntervalClassVector(Vector):
    r'''An interval-class vector.

    ..  container:: example

        ::

            >>> pitch_segment = pitchtools.PitchSegment(
            ...     items=[0, 11, 7, 4, 2, 9, 3, 8, 10, 1, 5, 6],
            ...     )
            >>> numbered_interval_class_vector = pitchtools.IntervalClassVector(
            ...     items=pitch_segment,
            ...     item_class=pitchtools.NumberedInversionEquivalentIntervalClass,
            ...     )
            >>> items = sorted(numbered_interval_class_vector.items())
            >>> for interval, count in items:
            ...     print(interval, count)
            ...
            1 12
            2 12
            3 12
            4 12
            5 12
            6 6

    '''

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        from abjad.tools import pitchtools
        prototype = (
            pitchtools.PitchSegment,
            pitchtools.PitchSet,
            pitchtools.PitchClassSegment,
            pitchtools.PitchClassSet,
            )
        if isinstance(items, prototype):
            intervals = []
            items = tuple(items)
            pairs = sequencetools.yield_all_unordered_pairs_of_sequence(items)
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
        r'''Gets interpreter representation of interval-class vector.

        ..  container:: example

            ::

                >>> segment = pitchtools.PitchSegment(
                ...     items=[0, 11, 7, 4, 2, 9, 3, 8, 10, 1, 5, 6],
                ...     )
                >>> vector = pitchtools.IntervalClassVector(
                ...     items=pitch_segment,
                ...     item_class=pitchtools.NumberedInversionEquivalentIntervalClass,
                ...     )

            ::

                >>> vector
                IntervalClassVector({'1': 12, '2': 12, '3': 12, '4': 12, '5': 12, '6': 6})

        Returns string.
        '''
        superclass = super(IntervalClassVector, self)
        return superclass.__repr__()

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedIntervalClass

    @property
    def _numbered_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedIntervalClass

    @property
    def _parent_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.IntervalClass

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(
        cls,
        selection,
        item_class=None,
        ):
        r'''Makes interval-class vector from `selection`.

        Returns interval-class vector.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        return cls(
            pitch_segment,
            item_class=item_class,
            )