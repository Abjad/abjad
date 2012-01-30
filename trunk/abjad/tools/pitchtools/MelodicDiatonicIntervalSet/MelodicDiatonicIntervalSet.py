from abjad.tools.pitchtools._IntervalSet import _IntervalSet


class MelodicDiatonicIntervalSet(_IntervalSet):
    '''.. versionadded:: 2.0

    Abjad model of melodic diatonic interval set::

        abjad> pitchtools.MelodicDiatonicIntervalSet('M2 M2 -m3 -P4')
        MelodicDiatonicIntervalSet('-P4 -m3 +M2')

    Melodic diatonic interval sets are immutable.
    '''

    def __new__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, str):
            interval_tokens = arg.split()
        else:
            interval_tokens = arg
        mdis = [pitchtools.MelodicDiatonicInterval(x) for x in interval_tokens]
        return frozenset.__new__(self, mdis)

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
        intervals = list(self.melodic_diatonic_intervals)
        intervals.sort(lambda x, y: cmp(x.number, y.number))
        return ' '.join([str(x) for x in intervals])

    ### PUBLIC ATTRIBUTES ###

    @property
    def harmonic_chromatic_interval_set(self):
        from abjad.tools import pitchtools
        return pitchtools.HarmonicChromaticIntervalSet(self)

    @property
    def harmonic_diatonic_interval_set(self):
        from abjad.tools import pitchtools
        return pitchtools.HarmonicDiatonicIntervalSet(self)

    @property
    def melodic_chromatic_interval_set(self):
        from abjad.tools import pitchtools
        return pitchtools.MelodicChromaticIntervalSet(self)

    @property
    def melodic_diatonic_interval_numbers(self):
        return set([interval.number for interval in self])

    @property
    def melodic_diatonic_intervals(self):
        return set(self)
