from abjad.tools.pitchtools._IntervalSegment import _IntervalSegment


class HarmonicDiatonicIntervalSegment(_IntervalSegment):
    '''.. versionadded:: 2.0

    Abjad model of harmonic diatonic interval segment::

        abjad> pitchtools.HarmonicDiatonicIntervalSegment('m2 M9 m3 M3')
        HarmonicDiatonicIntervalSegment('m2 M9 m3 M3')

    Harmonic diatonic interval segments are immutable.
    '''

    def __new__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, str):
            harmonic_diatonic_interval_tokens = arg.split()
        else:
            harmonic_diatonic_interval_tokens = arg
        hdis = []
        for token in harmonic_diatonic_interval_tokens:
            hdi = pitchtools.HarmonicDiatonicInterval(token)
            hdis.append(hdi)
        return tuple.__new__(self, hdis)

    ### OVERLOADS ###

    def __copy__(self):
        return type(self)(self.intervals)

    def __repr__(self):
        return "%s('%s')" % (type(self).__name__, ' '.join([str(x) for x in self]))

    ### PUBLIC ATTRIBUTES ###

    @property
    def harmonic_chromatic_interval_segment(self):
        from abjad.tools import pitchtools
        return pitchtools.HarmonicChromaticIntervalSegment(self)

    @property
    def melodic_chromatic_interval_segment(self):
        from abjad.tools import pitchtools
        return pitchtools.MelodicChromaticIntervalSegment(self)

    @property
    def melodic_diatonic_interval_segment(self):
        from abjad.tools import pitchtools
        return pitchtools.MelodicDiatonicIntervalSegment(self)
