# -*- coding: utf-8 -*-
from abjad.tools.pitchtools.Set import Set


class IntervalClassSet(Set):
    r'''Interval-class set.

    ::

        >>> import abjad

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        from abjad.tools import pitchtools
        prototype = (
            pitchtools.PitchClassSegment,
            pitchtools.PitchClassSet,
            pitchtools.PitchSegment,
            pitchtools.PitchSet,
            )
        if isinstance(items, prototype):
            items = list(items)
            enumerator = mathtools.Enumerator(items)
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
    def from_selection(class_, selection, item_class=None):
        r'''Initialize interval set from component selection:

        ::

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> staff_group = abjad.StaffGroup([staff_1, staff_2])
            >>> show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> f(staff_group)
            \new StaffGroup <<
                \new Staff {
                    c'4
                    <d' fs' a'>4
                    b2
                }
                \new Staff {
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
            NamedIntervalClass('-aug4')
            NamedIntervalClass('-M3')
            NamedIntervalClass('-m3')
            NamedIntervalClass('-M2')
            NamedIntervalClass('+m2')
            NamedIntervalClass('+M2')
            NamedIntervalClass('+m3')
            NamedIntervalClass('+M3')
            NamedIntervalClass('+P4')
            NamedIntervalClass('+aug4')
            NamedIntervalClass('+P5')
            NamedIntervalClass('+M6')
            NamedIntervalClass('+m7')
            NamedIntervalClass('+M7')
            NamedIntervalClass('+P8')

        Returns interval set.
        '''
        from abjad.tools import pitchtools
        interval_set = pitchtools.IntervalSet.from_selection(selection)
        return class_(
            items=interval_set,
            item_class=item_class,
            )
