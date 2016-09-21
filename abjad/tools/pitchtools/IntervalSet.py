# -*- coding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools.pitchtools.Set import Set


class IntervalSet(Set):
    r'''Interval set.
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

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
        r'''Initialize interval set from component selection:

        ::

            >>> staff_1 = Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = Staff("c4. r8 g2")
            >>> selection = select((staff_1, staff_2))
            >>> intervals = pitchtools.IntervalSet.from_selection(
            ...     selection)
            >>> for interval in sorted(intervals):
            ...     interval
            ...
            NamedInterval('-M6')
            NamedInterval('-P5')
            NamedInterval('-aug4')
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
            NamedInterval('+aug11')
            NamedInterval('+M13')

        Returns interval set.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        pairs = sequencetools.yield_all_unordered_pairs_of_sequence(
            pitch_segment)
        intervals = (second - first for first, second in pairs)
        return class_(
            items=intervals,
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
