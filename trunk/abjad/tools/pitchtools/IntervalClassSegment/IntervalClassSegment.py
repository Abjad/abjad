# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.pitchtools.Segment import Segment


class IntervalClassSegment(Segment):
    r'''Abjad model of an interval-class segment.
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

    ### PUBLIC PROPERTIES ###

    @property
    def is_tertian(self):
        r'''True when all diatonic interval-classes in segment are tertian.
        Otherwise false:

        ::

            >>> interval_class_segment = pitchtools.IntervalClassSegment(
            ...     tokens=[('major', 3), ('minor', 6), ('major', 6)],
            ...     item_class=pitchtools.NamedMelodicIntervalClass,
            ...     )
            >>> interval_class_segment.is_tertian
            True

        Return boolean.
        '''
        from abjad.tools import pitchtools
        inversion_equivalent_interval_class_segment = self.new(
            item_class=pitchtools.NamedInversionEquivalentIntervalClass,
            )
        for interval in inversion_equivalent_interval_class_segment:
            if not interval.number == 3:
                return False
        return True

