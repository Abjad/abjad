from abjad.tools.pitchtools._IntervalSegment import _IntervalSegment


class MelodicDiatonicIntervalSegment(_IntervalSegment):
    '''.. versionadded:: 2.0

    Abjad model of melodic diatonic interval segment::

        abjad> pitchtools.MelodicDiatonicIntervalSegment('M2 M9 -m3 -P4')
        MelodicDiatonicIntervalSegment('+M2 +M9 -m3 -P4')

    Melodic diatonic interval segments are immutable.
    '''

    def __new__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, str):
            melodic_diatonic_interval_tokens = arg.split()
        else:
            melodic_diatonic_interval_tokens = arg
        mdis = []
        for token in melodic_diatonic_interval_tokens:
            mdi = pitchtools.MelodicDiatonicInterval(token)
            mdis.append(mdi)
        return tuple.__new__(self, mdis)

    ### OVERLOADS ###

    def __copy__(self):
        return type(self)(self.intervals)

    def __repr__(self):
        return "%s('%s')" % (type(self).__name__, ' '.join([str(x) for x in self]))

    ### PUBLIC ATTRIBUTES ###

    @property
    def harmonic_chromatic_interval_segment(self):
        from abjad.tools import pitchtools
        return pitchtools.HarmonicChromaticIntervalSegment(self.intervals)

    @property
    def harmonic_diatonic_interval_segment(self):
        from abjad.tools import pitchtools
        return pitchtools.HarmonicDiatonicIntervalSegment(self.intervals)

    @property
    def melodic_chromatic_interval_segment(self):
        from abjad.tools import pitchtools
        return pitchtools.MelodicChromaticIntervalSegment(self.intervals)
