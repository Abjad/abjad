# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools.pitchtools.Set import Set


class IntervalSet(Set):
    r'''Abjad model of an interval set.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedMelodicInterval
    
    @property
    def _numbered_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedMelodicInterval

    @property
    def _parent_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.Interval

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(cls, selection, item_class=None, name=None):
        r'''Initialize interval set from component selection:

        ::

            >>> staff_1 = Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = Staff("c4. r8 g2")
            >>> selection = select((staff_1, staff_2))
            >>> intervals = pitchtools.IntervalSet.from_selection(
            ...     selection)
            >>> for interval in intervals:
            ...     interval
            ...
            NamedMelodicInterval('-aug4')
            NamedMelodicInterval('-m3')
            NamedMelodicInterval('+M7')
            NamedMelodicInterval('-M6')
            NamedMelodicInterval('+M9')
            NamedMelodicInterval('-M2')
            NamedMelodicInterval('+M13')
            NamedMelodicInterval('+aug11')
            NamedMelodicInterval('+m7')
            NamedMelodicInterval('-M3')
            NamedMelodicInterval('+P4')
            NamedMelodicInterval('+m3')
            NamedMelodicInterval('-P5')
            NamedMelodicInterval('+M3')
            NamedMelodicInterval('+P5')
            NamedMelodicInterval('+P8')
            NamedMelodicInterval('+m2')
        
        Return interval set.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        pairs = sequencetools.yield_all_unordered_pairs_of_sequence(
            pitch_segment)
        intervals = (second - first for first, second in pairs)
        return cls(
            tokens=intervals,
            item_class=item_class,
            name=name,
            )
