# -*- coding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.pitchtools.Segment import Segment
from abjad.tools.topleveltools import new


class IntervalClassSegment(Segment):
    r'''Interval-class segment.

    ..  container:: example

        **Example 1.** An interval-class segment:

        ::

            >>> intervals = 'm2 M10 -aug4 P5'
            >>> pitchtools.IntervalClassSegment(intervals)
            IntervalClassSegment(['+m2', '+M3', '-aug4', '+P5'])

    ..  container:: example

        **Example 2.** Another interval-class segment:

        ::

            >>> intervals = 'P4 P5 P11 P12'
            >>> pitchtools.IntervalClassSegment(intervals)
            IntervalClassSegment(['+P4', '+P5', '+P4', '+P5'])

    Returns interval-class segment.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(class_, selection, item_class=None):
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
        return class_(
            items=intervals,
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

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        return len(pitchtools.IntervalClassSet(
            self, item_class=self.item_class)) < len(self)

    @property
    def is_tertian(self):
        r'''Is true when all named interval-classes in segment are tertian.
        Otherwise false:

        ::

            >>> interval_class_segment = pitchtools.IntervalClassSegment(
            ...     items=[('major', 3), ('minor', 6), ('major', 6)],
            ...     item_class=pitchtools.NamedIntervalClass,
            ...     )
            >>> interval_class_segment.is_tertian
            True

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        inversion_equivalent_interval_class_segment = new(
            self,
            item_class=pitchtools.NamedInversionEquivalentIntervalClass,
            )
        for interval in inversion_equivalent_interval_class_segment:
            if not interval.number == 3:
                return False
        return True
