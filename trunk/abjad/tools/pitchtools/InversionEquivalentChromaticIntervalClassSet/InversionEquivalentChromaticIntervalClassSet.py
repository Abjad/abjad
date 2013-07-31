# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.IntervalClassSet import IntervalClassSet


class InversionEquivalentChromaticIntervalClassSet(IntervalClassSet):
    '''.. versionadded:: 2.0

    Abjad model of inversion-equivalent chromatic interval-class set:

    ::

        >>> pitchtools.InversionEquivalentChromaticIntervalClassSet(
        ...     [1, 1, 6, 2, 2])
        InversionEquivalentChromaticIntervalClassSet(1, 2, 6)

    Inversion-equivalent chromatic interval-class sets are immutable.
    '''

    ### CONSTRUCTOR ###

    def __new__(self, interval_class_tokens):
        from abjad.tools import pitchtools
        iecics = []
        for token in interval_class_tokens:
            iecic = pitchtools.InversionEquivalentChromaticIntervalClass(token)
            iecics.append(iecic)
        return frozenset.__new__(self, iecics)

    ### SPECIAL METHODS ###

    def __copy__(self):
        return type(self)(self.numbers)

    def __repr__(self):
        return '%s(%s)' % (self._class_name, self._format_string)

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return ', '.join([str(x) for x in sorted(
            self.inversion_equivalent_chromatic_interval_class_numbers)])

    ### PUBLIC PROPERTIES ###

    @property
    def inversion_equivalent_chromatic_interval_class_numbers(self):
        return set([interval_class.number for interval_class in self])

    @property
    def inversion_equivalent_chromatic_interval_classes(self):
        interval_classes = list(self)
        interval_classes.sort(key=lambda x: x.number)
        return interval_classes
