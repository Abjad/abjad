from .Set import Set


class IntervalClassSet(Set):
    """
    Interval-class set.
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
            enumerator = abjad.utilities.Enumerator(items)
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
    def from_selection(class_, selection, item_class=None):
        r"""
        Initialize interval set from component selection:

        ..  container:: example

            ::

                >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
                >>> staff_2 = abjad.Staff("c4. r8 g2")
                >>> staff_group = abjad.StaffGroup([staff_1, staff_2])
                >>> abjad.show(staff_group) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff_group)
                \new StaffGroup
                <<
                    \new Staff
                    {
                        c'4
                        <d' fs' a'>4
                        b2
                    }
                    \new Staff
                    {
                        c4.
                        r8
                        g2
                    }
                >>

            ::

                >>> interval_classes = abjad.IntervalClassSet.from_selection(
                ...     staff_group)
                >>> for interval_class in sorted(interval_classes):
                ...     interval_class
                ...
                NamedIntervalClass('-M6')
                NamedIntervalClass('-P5')
                NamedIntervalClass('-A4')
                NamedIntervalClass('-M3')
                NamedIntervalClass('-m3')
                NamedIntervalClass('-M2')
                NamedIntervalClass('+m2')
                NamedIntervalClass('+M2')
                NamedIntervalClass('+m3')
                NamedIntervalClass('+M3')
                NamedIntervalClass('+P4')
                NamedIntervalClass('+A4')
                NamedIntervalClass('+P5')
                NamedIntervalClass('+M6')
                NamedIntervalClass('+m7')
                NamedIntervalClass('+M7')
                NamedIntervalClass('+P8')

        Returns interval set.
        """
        import abjad
        interval_set = abjad.IntervalSet.from_selection(selection)
        return class_(
            items=interval_set,
            item_class=item_class,
            )
