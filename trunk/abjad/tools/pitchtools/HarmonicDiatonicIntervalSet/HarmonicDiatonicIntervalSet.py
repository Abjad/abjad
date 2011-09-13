from abjad.tools.pitchtools._IntervalSet import _IntervalSet


class HarmonicDiatonicIntervalSet(_IntervalSet):
    '''.. versionadded:: 2.0

    Abjad model of harmonic diatonic interval set::

        abjad> pitchtools.HarmonicDiatonicIntervalSet('m2 m2 M2 M9')
        HarmonicDiatonicIntervalSet('m2 M2 M9')

    Harmonic diatonic interval sets are immutable.
    '''

    def __new__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, str):
            interval_tokens = arg.split()
        else:
            interval_tokens = arg
        hdis = [pitchtools.HarmonicDiatonicInterval(x) for x in interval_tokens]
        return frozenset.__new__(self, hdis)

    ### OVERLOADS ###

    def __copy__(self):
        return type(self)(self)

    def __repr__(self):
        return "%s('%s')" % (type(self).__name__, self._format_string)

    def __str__(self):
        return '{%s}' % self._format_string

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_string(self):
        return ' '.join([str(x) for x in sorted(self.harmonic_diatonic_intervals)])

    ### PUBLIC ATTRIBUTES ###

    @property
    def harmonic_chromatic_interval_set(self):
        from abjad.tools import pitchtools
        return pitchtools.HarmonicChromaticIntervalSet(self)

    @property
    #def intervals(self):
    def harmonic_diatonic_intervals(self):
        return set(self)

    @property
    #def numbers(self):
    def harmonic_diatonic_interval_numbers(self):
        return set([interval.number for interval in self])
