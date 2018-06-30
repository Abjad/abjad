from abjad.utilities.Enumerator import Enumerator
from .Set import Set


class IntervalSet(Set):
    """
    Interval set.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        import abjad
        prototype = (
            abjad.PitchClassSegment,
            abjad.PitchClassSet,
            abjad.PitchSegment,
            abjad.PitchSet,
            )
        if isinstance(items, prototype):
            items = list(items)
            enumerator = Enumerator(items)
            pairs = enumerator.yield_pairs()
            items = [second - first for first, second in pairs]
        Set.__init__(
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

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
        """
        Initializes interval set from component selection.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> selection = abjad.select((staff_1, staff_2))
            >>> intervals = abjad.IntervalSet.from_selection(selection)
            >>> for interval in sorted(intervals):
            ...     interval
            ...
            NamedInterval('-M6')
            NamedInterval('-P5')
            NamedInterval('-A4')
            NamedInterval('-M3')
            NamedInterval('-m3')
            NamedInterval('-M2')
            NamedInterval('+m2')
            NamedInterval('+m3')
            NamedInterval('+M3')
            NamedInterval('+P4')
            NamedInterval('+P5')
            NamedInterval('+m7')
            NamedInterval('+M7')
            NamedInterval('+P8')
            NamedInterval('+M9')
            NamedInterval('+A11')
            NamedInterval('+M13')

        Returns interval set.
        """
        import abjad
        pitch_segment = abjad.PitchSegment.from_selection(selection)
        enumerator = Enumerator(pitch_segment)
        pairs = enumerator.yield_pairs()
        intervals = [second - first for first, second in pairs]
        return class_(
            items=intervals,
            item_class=item_class,
            )
