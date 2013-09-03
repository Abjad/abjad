# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.Set import Set


class IntervalClassSet(Set):
    r'''Abjad model of an interval-class set.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedMelodicIntervalClass
    
    @property
    def _numbered_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedMelodicIntervalClass

    @property
    def _parent_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.IntervalClass
        
    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(cls, selection, item_class=None, name=None):
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
            NamedMelodicIntervalClass('-M3')
            NamedMelodicIntervalClass('+m7')
            NamedMelodicIntervalClass('+P5')
            NamedMelodicIntervalClass('+P4')
            NamedMelodicIntervalClass('+m3')
            NamedMelodicIntervalClass('+M7')
            NamedMelodicIntervalClass('-M6')
            NamedMelodicIntervalClass('-aug4')
            NamedMelodicIntervalClass('+M6')
            NamedMelodicIntervalClass('+P8')
            NamedMelodicIntervalClass('-P5')
            NamedMelodicIntervalClass('+M2')
            NamedMelodicIntervalClass('+M3')
            NamedMelodicIntervalClass('-M2')
            NamedMelodicIntervalClass('+aug4')
            NamedMelodicIntervalClass('+m2')
            NamedMelodicIntervalClass('-m3')
        
        Return interval set.
        '''
        from abjad.tools import pitchtools
        interval_set = pitchtools.IntervalSet.from_selection(selection)
        return cls(
            tokens=interval_set,
            item_class=item_class,
            name=name,
            )
