# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.pitchtools.IntervalSegment import IntervalSegment


class NumberedMelodicIntervalSegment(IntervalSegment):
    '''Abjad model of melodic chromatic interval segment:

    ::

        >>> pitchtools.NumberedMelodicIntervalSegment(
        ...     [11, 13, 13.5, -2, 2.5])
        NumberedMelodicIntervalSegment(+11, +13, +13.5, -2, +2.5)

    Melodic chromatic interval segments are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools
        IntervalSegment.__init__(
            self,
            tokens=tokens,
            item_class=pitchtools.NumberedMelodicInterval,
            name=None,
            )

    ### SPECIAL METHODS ###

    def __copy__(self):
        return type(self)(self.intervals)

    ### PUBLIC PROPERTIES ###

    @property
    def slope(self):
        r'''The slope of a melodic interval segment is the sum of its 
        intervals divided by its length:

        ::

            >>> pitchtools.NumberedMelodicIntervalSegment([1, 2]).slope
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

            >>> pitchtools.NumberedMelodicIntervalSegment(
            ...     [1, 2, -3, 1, -2, 1]).spread
            NumberedHarmonicInterval(4.0)
            >>> pitchtools.NumberedMelodicIntervalSegment(
            ...     [1, 1, 1, 2, -3, -2]).spread
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
