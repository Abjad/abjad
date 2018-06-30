from abjad import mathtools
from abjad.top.new import new
from abjad.utilities.Multiplier import Multiplier
from .Segment import Segment


class IntervalSegment(Segment):
    """
    Interval segment.

    ..  container:: example

        Initializes from string:

        >>> intervals = 'm2 M10 -aug4 P5'
        >>> abjad.IntervalSegment(intervals)
        IntervalSegment(['+m2', '+M10', '-A4', '+P5'])

    ..  container:: example

        Initializes from pitch segment:

        >>> pitch_segment = abjad.PitchSegment("c d e f g a b c'")
        >>> abjad.IntervalSegment(pitch_segment)
        IntervalSegment(['+M2', '+M2', '+m2', '+M2', '+M2', '+M2', '+m2'])

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        import abjad
        if isinstance(items, abjad.PitchSegment):
            intervals = []
            for one, two in abjad.sequence(items).nwise():
                intervals.append(one - two)
            items = intervals
        Segment.__init__(
            self,
            items=items,
            item_class=item_class,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        import abjad
        return abjad.NamedInterval

    @property
    def _numbered_item_class(self):
        import abjad
        return abjad.NumberedInterval

    @property
    def _parent_item_class(self):
        import abjad
        return abjad.Interval

    ### PUBLIC PROPERTIES ###

    @property
    def slope(self):
        """
        Gets slope of interval segment.

        ..  container:: example

            The slope of a interval segment is the sum of its
            intervals divided by its length:

            >>> abjad.IntervalSegment([1, 2]).slope
            Multiplier(3, 2)

        Returns multiplier.
        """
        result = sum([x.number for x in self]) / len(self)
        return Multiplier.from_float(result)

    @property
    def spread(self):
        """
        Gets spread of interval segment.

        ..  container:: example

            The maximum interval spanned by any combination of
            the intervals within a numbered interval segment.

            >>> abjad.IntervalSegment([1, 2, -3, 1, -2, 1]).spread
            NumberedInterval(4)

            >>> abjad.IntervalSegment([1, 1, 1, 2, -3, -2]).spread
            NumberedInterval(5)

        Returns numbered interval.
        """
        import abjad
        current = maximum = minimum = 0
        for x in self:
            current += float(x.number)
            if maximum < current:
                maximum = current
            if current < minimum:
                minimum = current
        return abjad.NumberedInterval(maximum - minimum)

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        """
        Makes interval segment from component `selection`.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
            >>> abjad.IntervalSegment.from_selection(
            ...     staff,
            ...     item_class=abjad.NumberedInterval,
            ...     )
            IntervalSegment([2, 2, 1, 2, 2, 2, 1])

        Returns interval segment.
        """
        import abjad
        pitch_segment = abjad.PitchSegment.from_selection(selection)
        pitches = [_ for _ in pitch_segment]
        intervals = (-x for x in mathtools.difference_series(pitches))
        return class_(
            items=intervals,
            item_class=item_class,
            )

    def has_duplicates(self):
        """
        Is true if segment has duplicate items.

        ..  container:: example

            >>> intervals = 'm2 M3 -aug4 m2 P5'
            >>> segment = abjad.IntervalSegment(intervals)
            >>> segment.has_duplicates()
            True

            >>> intervals = 'M3 -aug4 m2 P5'
            >>> segment = abjad.IntervalSegment(intervals)
            >>> segment.has_duplicates()
            False

        Returns true or false.
        """
        import abjad
        return len(abjad.IntervalSet(self)) < len(self)

    def rotate(self, n=0):
        """
        Rotates interval segment by index `n`.

        Returns new interval segment.
        """
        return new(self, self[-n:] + self[:-n])
