from abjad.utilities.Enumerator import Enumerator
from .Vector import Vector


class IntervalClassVector(Vector):
    """
    Interval-class vector.

    ..  container:: example

        An interval-class vector:

        >>> pitch_segment = abjad.PitchSegment(
        ...     items=[0, 11, 7, 4, 2, 9, 3, 8, 10, 1, 5, 6],
        ...     )
        >>> numbered_interval_class_vector = abjad.IntervalClassVector(
        ...     items=pitch_segment,
        ...     item_class=abjad.NumberedInversionEquivalentIntervalClass,
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

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        import abjad
        prototype = (
            abjad.PitchSegment,
            abjad.PitchSet,
            abjad.PitchClassSegment,
            abjad.PitchClassSet,
            )
        if isinstance(items, prototype):
            intervals = []
            items = tuple(items)
            enumerator = Enumerator(items)
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
        """
        Gets interpreter representation of interval-class vector.

        ..  container:: example

            Gets interpreter representation of interval-class vector:

            >>> pitch_segment = abjad.PitchSegment(
            ...     items=[0, 11, 7, 4, 2, 9, 3, 8, 10, 1, 5, 6],
            ...     )
            >>> vector = abjad.IntervalClassVector(
            ...     items=pitch_segment,
            ...     item_class=abjad.NumberedInversionEquivalentIntervalClass,
            ...     )

            >>> vector
            IntervalClassVector({1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 6}, item_class=NumberedInversionEquivalentIntervalClass)

        ..  container:: example

            Initializes from interpreter representation of interval-class
            vector:

            >>> abjad.IntervalClassVector(vector)
            IntervalClassVector({1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 6}, item_class=NumberedInversionEquivalentIntervalClass)

        Returns string.
        """
        return super().__repr__()

    ### PRIVATE PROPERTIES ###

    @property
    def _label(self):
        counts = []
        for i in range(7):
            counts.append(self[i])
        counts = ''.join([str(x) for x in counts])
        if len(self) == 13:
            quartertones = []
            for i in range(6):
                quartertones.append(self[i + 0.5])
            quartertones = ''.join([str(x) for x in quartertones])
            return r'\tiny \column { "%s" "%s" }' % (counts, quartertones)
        else:
            return r'\tiny %s' % counts

    @property
    def _named_item_class(self):
        import abjad
        return abjad.NamedIntervalClass

    @property
    def _numbered_item_class(self):
        import abjad
        return abjad.NumberedIntervalClass

    @property
    def _parent_item_class(self):
        import abjad
        return abjad.IntervalClass

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        """
        Makes interval-class vector from `selection`.

        ..  container:: example

            Makes numbered inversion-equivalent interval-class vector from
            selection:

            >>> vector = abjad.IntervalClassVector.from_selection(
            ...     abjad.Chord("<c' d' b''>4"),
            ...     item_class=abjad.NumberedInversionEquivalentIntervalClass,
            ...     )
            >>> vector
            IntervalClassVector({1: 1, 2: 1, 3: 1}, item_class=NumberedInversionEquivalentIntervalClass)

        ..  container:: example

            Makes numbered interval-class vector from selection:

            >>> vector = abjad.IntervalClassVector.from_selection(
            ...     abjad.Chord("<c' d' b''>4"),
            ...     item_class=abjad.NumberedIntervalClass,
            ...     )
            >>> vector
            IntervalClassVector({-11: 1, -9: 1, -2: 1}, item_class=NumberedIntervalClass)

            .. todo:: This should probabaly be checked. Resulting values
                should probabaly be positive (or signless) instead of negative.

        ..  container:: example

            Makes named interval-class vector from selection:

            >>> vector = abjad.IntervalClassVector.from_selection(
            ...     abjad.Chord("<c' d' b''>4"),
            ...     item_class=None,
            ...     )
            >>> vector
            IntervalClassVector({'-M2': 1, '-M6': 1, '-M7': 1}, item_class=NamedIntervalClass)

            .. todo:: This should probabaly be checked. Resulting values
                should probabaly be positive (or signless) instead of negative.

        Returns new interval-class vector.
        """
        import abjad
        pitch_segment = abjad.PitchSegment.from_selection(selection)
        return class_(
            pitch_segment,
            item_class=item_class,
            )
