from abjad.tools.pitchtools._IntervalClassSet import _IntervalClassSet


class HarmonicDiatonicIntervalClassSet(_IntervalClassSet):
    '''.. versionadded:: 2.0

    Abjad model of harmonic diatonic interval-class set::

        abjad> pitchtools.HarmonicDiatonicIntervalClassSet('m2 M2 m3 M3') # doctest: +SKIP
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
        return ' '.join([str(x) for x in sorted(self.harmonic_diatonic_interval_classes)])

    ### PUBLIC ATTRIBUTES ###

    @property
    #def interval_classes(self):
    def harmonic_diatonic_interval_classes(self):
        return set(self)
