from abjad.tools.pitchtools._IntervalSegment import _IntervalSegment
import fractions


class MelodicChromaticIntervalSegment(_IntervalSegment):
    '''.. versionadded:: 2.0

    Abjad model of melodic chromatic interval segment::

        abjad> pitchtools.MelodicChromaticIntervalSegment([11, 13, 13.5, -2, 2.5])
        MelodicChromaticIntervalSegment(+11, +13, +13.5, -2, +2.5)

    Melodic chromatic interval segments are immutable.
    '''

    def __new__(self, mci_tokens):
        from abjad.tools import pitchtools
        mcis = []
        for token in mci_tokens:
            mci = pitchtools.MelodicChromaticInterval(token)
            mcis.append(mci)
        return tuple.__new__(self, mcis)

    ### OVERLOADS ###

    def __copy__(self):
        return type(self)(self.intervals)

    ### PUBLIC ATTRIBUTES ###

    @property
    def harmonic_chromatic_interval_segment(self):
        from abjad.tools import pitchtools
        return pitchtools.HarmonicChromaticIntervalSegment(self)

    @property
    def melodic_chromatic_interval_class_segment(self):
        from abjad.tools import pitchtools
        return pitchtools.MelodicChromaticIntervalClassSegment(self)

    @property
    def melodic_chromatic_interval_numbers(self):
        return tuple([mci.number for mci in self])

    @property
    def melodic_chromatic_interval_class_vector(self):
        from abjad.tools import pitchtools
        return pitchtools.MelodicChromaticIntervalClassVector(self)

    @property
    def slope(self):
        '''The slope of a melodic interval segment is the sum of its intervals
        divided by its length::

            abjad> pitchtools.MelodicChromaticIntervalSegment([1, 2]).slope
            Fraction(3, 2)

        Return fraction.
        '''
        return fractions.Fraction.from_float(sum([x.number for x in self])) / len(self)

    @property
    def spread(self):
        '''The maximum harmonic interval spanned by any combination of the intervals within
        a harmonic chromatic interval segment::

            abjad> pitchtools.MelodicChromaticIntervalSegment([1, 2, -3, 1, -2, 1]).spread
            HarmonicChromaticInterval(4)
            abjad> pitchtools.MelodicChromaticIntervalSegment([1, 1, 1, 2, -3, -2]).spread
            HarmonicChromaticInterval(5)

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
        return pitchtools.HarmonicChromaticInterval(maximum - minimum)
