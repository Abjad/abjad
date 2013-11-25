# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.pitchtools.Segment import Segment


class IntervalClassSegment(Segment):
    r'''An interval-class segment.

    ::

        >>> intervals = 'm2 M10 -aug4 P5'
        >>> pitchtools.IntervalClassSegment(intervals)
        IntervalClassSegment(['+m2', '+M3', '-aug4', '+P5'])

    Returns interval-class segment.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

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
    def from_selection(cls, selection, item_class=None, custom_identifier=None):
        r'''Initialize interval-class segment from component selection:

        ::

            >>> staff_1 = Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = Staff("c4. r8 g2")
            >>> selection = select((staff_1, staff_2))
            >>> pitchtools.IntervalClassSegment.from_selection(selection)
            IntervalClassSegment(['-M2', '-M3', '-m3', '+m7', '+M7', '-P5'])        

        Returns interval-class segment.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        intervals = mathtools.difference_series(pitch_segment)
        return cls(
            tokens=intervals,
            item_class=item_class,
            custom_identifier=custom_identifier,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def has_duplicates(self):
        r'''True if segment contains duplicate items:

        ::

            >>> intervals = 'm2 M3 -aug4 m2 P5'
            >>> segment = pitchtools.IntervalClassSegment(intervals)
            >>> segment.has_duplicates
            True

        ::

            >>> intervals = 'M3 -aug4 m2 P5'
            >>> segment = pitchtools.IntervalClassSegment(intervals)
            >>> segment.has_duplicates
            False

        Returns boolean.
        '''
        from abjad.tools import pitchtools
        return len(pitchtools.IntervalClassSet(
            self, item_class=self.item_class)) < len(self)

    @property
    def is_tertian(self):
        r'''True when all diatonic interval-classes in segment are tertian.
        Otherwise false:

        ::

            >>> interval_class_segment = pitchtools.IntervalClassSegment(
            ...     tokens=[('major', 3), ('minor', 6), ('major', 6)],
            ...     item_class=pitchtools.NamedIntervalClass,
            ...     )
            >>> interval_class_segment.is_tertian
            True

        Returns boolean.
        '''
        from abjad.tools import pitchtools
        inversion_equivalent_interval_class_segment = self.__makenew__(
            item_class=pitchtools.NamedInversionEquivalentIntervalClass,
            )
        for interval in inversion_equivalent_interval_class_segment:
            if not interval.number == 3:
                return False
        return True
