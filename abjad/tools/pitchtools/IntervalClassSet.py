# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools.pitchtools.Set import Set


class IntervalClassSet(Set):
    r'''An interval-class set.
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
            pairs = sequencetools.yield_all_unordered_pairs_of_sequence(
                items)
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
    def from_selection(cls, selection, item_class=None):
        r'''Initialize interval set from component selection:

        ::

            >>> staff_1 = Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = Staff("c4. r8 g2")
            >>> selection = select((staff_1, staff_2))
            >>> interval_classes = pitchtools.IntervalClassSet.from_selection(
            ...     selection)
            >>> for interval_class in interval_classes:
            ...     interval_class
            ...
            NamedIntervalClass('-aug4')
            NamedIntervalClass('+m7')
            NamedIntervalClass('+M3')
            NamedIntervalClass('-M2')
            NamedIntervalClass('+m3')
            NamedIntervalClass('+M7')
            NamedIntervalClass('+M6')
            NamedIntervalClass('-m3')
            NamedIntervalClass('-M3')
            NamedIntervalClass('+aug4')
            NamedIntervalClass('+P4')
            NamedIntervalClass('+M2')
            NamedIntervalClass('+P8')
            NamedIntervalClass('-P5')
            NamedIntervalClass('+P5')
            NamedIntervalClass('-M6')
            NamedIntervalClass('+m2')

        Returns interval set.
        '''
        from abjad.tools import pitchtools
        interval_set = pitchtools.IntervalSet.from_selection(selection)
        return cls(
            items=interval_set,
            item_class=item_class,
            )
