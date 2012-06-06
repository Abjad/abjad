from abjad.tools.pitchtools.IntervalObjectSet import IntervalObjectSet


class HarmonicChromaticIntervalSet(IntervalObjectSet):
    '''.. versionadded:: 2.0

    Abjad model of harmonic chromatic interval set::

        >>> pitchtools.HarmonicChromaticIntervalSet([10, -12, -13, -13, -13.5])
        HarmonicChromaticIntervalSet(10, 12, 13, 13.5)

    Harmonic chromatic interval sets are immutable.
    '''

    ### INITIALIZER ###

    def __new__(self, interval_tokens):
        from abjad.tools import pitchtools
        hcis = []
        for token in interval_tokens:
            hci = pitchtools.HarmonicChromaticInterval(token)
            hcis.append(hci)
        return frozenset.__new__(self, hcis)

    ### SPECIAL METHODS ###

    def __copy__(self):
        return type(self)(self)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._format_string)

    def __str__(self):
        return '{%s}' % self._format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return ', '.join([str(x) for x in sorted(self.harmonic_chromatic_intervals)])

    ### PUBLIC PROPERTIES ###

    @property
    def harmonic_chromatic_interval_numbers(self):
        return set([interval.number for interval in self])

    @property
    def harmonic_chromatic_intervals(self):
        return set(self)
