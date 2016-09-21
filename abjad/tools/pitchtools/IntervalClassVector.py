# -*- coding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools.pitchtools.Vector import Vector


class IntervalClassVector(Vector):
    r'''Interval-class vector.

    ..  container:: example

        **Example 1.** An interval-class vector:

        ::

            >>> pitch_segment = pitchtools.PitchSegment(
            ...     items=[0, 11, 7, 4, 2, 9, 3, 8, 10, 1, 5, 6],
            ...     )
            >>> numbered_interval_class_vector = pitchtools.IntervalClassVector(
            ...     items=pitch_segment,
            ...     item_class=pitchtools.NumberedInversionEquivalentIntervalClass,
            ...     )

        ::

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

            **Example 1.** Gets interpreter representation of interval-class
            vector:

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
                IntervalClassVector({1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 6}, item_class=NumberedInversionEquivalentIntervalClass)

        ..  container:: example

            **Example 2.** Initializes from interpreter representation of
            interval-class vector:

            ::

                >>> pitchtools.IntervalClassVector(vector)
                IntervalClassVector({1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 6}, item_class=NumberedInversionEquivalentIntervalClass)

        Returns string.
        '''
        superclass = super(IntervalClassVector, self)
        return superclass.__repr__()

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        r'''Makes interval-class vector from `selection`.

        ..  container:: example

            **Example 1.** Makes numbered inversion-equivalent interval-class
            vector from selection:

            ::

                >>> vector = pitchtools.IntervalClassVector.from_selection(
                ...     Chord("<c' d' b''>4"),
                ...     item_class=pitchtools.NumberedInversionEquivalentIntervalClass,
                ...     )
                >>> vector
                IntervalClassVector({1: 1, 2: 1, 3: 1}, item_class=NumberedInversionEquivalentIntervalClass)

        ..  container:: example

            **Example 2.** Makes numbered interval-class vector from selection:

            ::

                >>> vector = pitchtools.IntervalClassVector.from_selection(
                ...     Chord("<c' d' b''>4"),
                ...     item_class=pitchtools.NumberedIntervalClass,
                ...     )
                >>> vector
                IntervalClassVector({-11: 1, -9: 1, -2: 1}, item_class=NumberedIntervalClass)

            .. todo:: This should probabaly be checked. Resulting values
                should probabaly be positive (or signless) instead of negative.

        ..  container:: example

            **Example 3.** Makes named interval-class vector from selection:

            ::

                >>> vector = pitchtools.IntervalClassVector.from_selection(
                ...     Chord("<c' d' b''>4"),
                ...     item_class=None,
                ...     )
                >>> vector
                IntervalClassVector({'-M2': 1, '-M6': 1, '-M7': 1}, item_class=NamedIntervalClass)

            .. todo:: This should probabaly be checked. Resulting values
                should probabaly be positive (or signless) instead of negative.

        Returns new interval-class vector.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        return class_(
            pitch_segment,
            item_class=item_class,
            )

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
