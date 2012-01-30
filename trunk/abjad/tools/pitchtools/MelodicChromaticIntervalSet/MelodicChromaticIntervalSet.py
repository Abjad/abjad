from abjad.tools.pitchtools._IntervalSet import _IntervalSet


class MelodicChromaticIntervalSet(_IntervalSet):
    '''.. versionadded:: 2.0

    Abjad model of melodic chromatic interval set::

        abjad> pitchtools.MelodicChromaticIntervalSet([11, 11, 13.5, 13.5])
        MelodicChromaticIntervalSet(+11, +13.5)

    Melodic chromatic interval sets are immutable.
    '''

    def __new__(self, interval_tokens):
        from abjad.tools import pitchtools
        mcis = [pitchtools.MelodicChromaticInterval(x) for x in interval_tokens]
        return frozenset.__new__(self, mcis)

    ### OVERLOADS ###

    def __copy__(self):
        return type(self)(self)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._format_string)

    def __str__(self):
        return '{%s}' % self._format_string

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_string(self):
        intervals = list(self.melodic_chromatic_intervals)
        intervals.sort(lambda x, y: cmp(x.number, y.number))
        return ', '.join([str(x) for x in intervals])

    ### PUBLIC ATTRIBUTES ###

    @property
    def harmonic_chromatic_interval_set(self):
        from abjad.tools import pitchtools
        return pitchtools.HarmonicChromaticIntervalSet(self)

    @property
    def melodic_chromatic_interval_numbers(self):
        return set([interval.number for interval in self])

    @property
    def melodic_chromatic_intervals(self):
        return set(self)
