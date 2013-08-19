# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.IntervalSegment import IntervalSegment
import fractions


class NumberedMelodicIntervalSegment(IntervalSegment):
    '''Abjad model of melodic chromatic interval segment:

    ::

        >>> pitchtools.NumberedMelodicIntervalSegment(
        ...     [11, 13, 13.5, -2, 2.5])
        NumberedMelodicIntervalSegment(+11, +13, +13.5, -2, +2.5)

    Melodic chromatic interval segments are immutable.
    '''

    ### CONSTRUCTOR ###

    def __new__(cls, mci_tokens):
        from abjad.tools import pitchtools
        mcis = []
        for token in mci_tokens:
            mci = pitchtools.NumberedMelodicInterval(token)
            mcis.append(mci)
        return tuple.__new__(cls, mcis)

    ### SPECIAL METHODS ###

    def __copy__(self):
        return type(self)(self.intervals)

    ### PUBLIC PROPERTIES ###

    @property
    def harmonic_chromatic_interval_segment(self):
        from abjad.tools import pitchtools
        return pitchtools.HarmonicChromaticIntervalSegment(self)

    @property
    def melodic_chromatic_interval_class_segment(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedMelodicIntervalClassSegment(self)

    @property
    def melodic_chromatic_interval_class_vector(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedMelodicIntervalClassVector(self)

    @property
    def melodic_chromatic_interval_numbers(self):
        return tuple([mci.number for mci in self])

    @property
    def slope(self):
        r'''The slope of a melodic interval segment is the sum of its 
        intervals divided by its length:

        ::

            >>> pitchtools.NumberedMelodicIntervalSegment([1, 2]).slope
            Fraction(3, 2)

        Return fraction.
        '''
        return fractions.Fraction.from_float(
            sum([x.number for x in self])) / len(self)

    @property
    def spread(self):
        r'''The maximum harmonic interval spanned by any combination of 
        the intervals within a harmonic chromatic interval segment:

        ::

            >>> pitchtools.NumberedMelodicIntervalSegment(
            ...     [1, 2, -3, 1, -2, 1]).spread
            NumberedHarmonicInterval(4)
            >>> pitchtools.NumberedMelodicIntervalSegment(
            ...     [1, 1, 1, 2, -3, -2]).spread
            NumberedHarmonicInterval(5)

        Return harmonic chromatic interval.
        '''
        from abjad.tools import pitchtools
        current = maximum = minimum = 0
        for x in self.melodic_chromatic_interval_numbers:
            current += x
            if maximum < current:
                maximum = current
            if current < minimum:
                minimum = current
        return pitchtools.NumberedHarmonicInterval(maximum - minimum)
