# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.pitchtools.Segment import Segment


class IntervalSegment(Segment):
    r'''Abjad model of an interval segment.
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
        r'''Initialize interval segment from component selection:

        ::

            >>> staff_1 = Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = Staff("c4. r8 g2")
            >>> selection = select((staff_1, staff_2))
            >>> pitchtools.IntervalSegment.from_selection(selection)
            IntervalSegment(['-M2', '-M3', '-m3', '+m7', '+M7', '-P5'])
        
        Return interval segment.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        intervals = mathtools.difference_series(pitch_segment)
        return cls(
            tokens=intervals,
            item_class=item_class,
            name=name,
            )

    def rotate(self, n):
        return self.new(self[-n:] + self[:-n])

    ### PUBLIC PROPERTIES ###

    @property
    def slope(self):
        r'''The slope of a melodic interval segment is the sum of its 
        intervals divided by its length:

        ::

            >>> pitchtools.IntervalSegment([1, 2]).slope
            Multiplier(3, 2)

        Return multiplier.
        '''
        return durationtools.Multiplier.from_float(
            sum([x.number for x in self])) / len(self)

    @property
    def spread(self):
        r'''The maximum harmonic interval spanned by any combination of 
        the intervals within a harmonic chromatic interval segment:

        ::

            >>> pitchtools.IntervalSegment([1, 2, -3, 1, -2, 1]).spread
            NumberedHarmonicInterval(4.0)

        ::

            >>> pitchtools.IntervalSegment([1, 1, 1, 2, -3, -2]).spread
            NumberedHarmonicInterval(5.0)

        Return harmonic chromatic interval.
        '''
        from abjad.tools import pitchtools
        current = maximum = minimum = 0
        for x in self:
            current += float(x)
            if maximum < current:
                maximum = current
            if current < minimum:
                minimum = current
        return pitchtools.NumberedHarmonicInterval(maximum - minimum)
