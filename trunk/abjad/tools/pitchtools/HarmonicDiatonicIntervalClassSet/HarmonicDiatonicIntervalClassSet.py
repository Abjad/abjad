from abjad.tools.pitchtools.IntervalClassObjectSet import IntervalClassObjectSet


class HarmonicDiatonicIntervalClassSet(IntervalClassObjectSet):
    '''.. versionadded:: 2.0

    Abjad model of harmonic diatonic interval-class set::

        >>> pitchtools.HarmonicDiatonicIntervalClassSet('m2 M2 m3 M3') # doctest: +SKIP
        HarmonicDiatonicIntervalClassSet('m2 M2 m3 M3')

    Harmonic diatonic interval-class sets are immutable.
    '''

    def __new__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, str):
            interval_tokens = arg.split()
        else:
            interval_tokens = arg
        hdics = [pitchtools.HarmonicDiatonicIntervalClass(x) for x in interval_tokens]
        return frozenset.__new__(self, hdics)

    ### SPECIAL METHODS ###

    def __copy__(self):
        return type(self)(self)

    def __repr__(self):
        return "%s('%s')" % (type(self).__name__, self._format_string)

    def __str__(self):
        return '{%s}' % self._format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return ' '.join([str(x) for x in sorted(self.harmonic_diatonic_interval_classes)])

    ### PUBLIC PROPERTIES ###

    @property
    #def interval_classes(self):
    def harmonic_diatonic_interval_classes(self):
        return set(self)
