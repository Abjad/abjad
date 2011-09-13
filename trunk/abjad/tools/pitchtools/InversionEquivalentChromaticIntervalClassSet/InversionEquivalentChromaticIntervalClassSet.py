from abjad.tools.pitchtools._IntervalClassSet import _IntervalClassSet


class InversionEquivalentChromaticIntervalClassSet(_IntervalClassSet):
    '''.. versionadded:: 2.0

    Abjad model of inversion-equivalent chromatic interval-class set::

        abjad> pitchtools.InversionEquivalentChromaticIntervalClassSet([1, 1, 6, 2, 2])
        InversionEquivalentChromaticIntervalClassSet(1, 2, 6)

    Inversion-equivalent chromatic interval-class sets are immutable.
    '''

    def __new__(self, interval_class_tokens):
        from abjad.tools import pitchtools
        iecics = []
        for token in interval_class_tokens:
            iecic = pitchtools.InversionEquivalentChromaticIntervalClass(token)
            iecics.append(iecic)
        return frozenset.__new__(self, iecics)

    ### OVERLOADS ###

    def __copy__(self):
        return type(self)(self.numbers)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._format_string)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_string(self):
        return ', '.join([str(x) for x in sorted(self.inversion_equivalent_chromatic_interval_class_numbers)])

    ### PUBLIC ATTRIBUTES ###

    @property
    #def interval_classes(self):
    def inversion_equivalent_chromatic_interval_classes(self):
        interval_classes = list(self)
        interval_classes.sort(lambda x, y: cmp(x.number, y.number))
        return interval_classes

    @property
    #def numbers(self):
    def inversion_equivalent_chromatic_interval_class_numbers(self):
        return set([interval_class.number for interval_class in self])
