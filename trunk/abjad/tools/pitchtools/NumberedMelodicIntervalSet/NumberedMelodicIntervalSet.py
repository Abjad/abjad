# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.Set import Set


class NumberedMelodicIntervalSet(Set):
    '''Abjad model of melodic chromatic interval set:

    ::

        >>> pitchtools.NumberedMelodicIntervalSet([11, 11, 13.5, 13.5])
        NumberedMelodicIntervalSet(+11, +13.5)

    Melodic chromatic interval sets are immutable.
    '''

    ### CONSTRUCTOR ###

    def __new__(self, interval_tokens):
        from abjad.tools import pitchtools
        mcis = [pitchtools.NumberedMelodicInterval(x) 
            for x in interval_tokens]
        return frozenset.__new__(self, mcis)

    ### SPECIAL METHODS ###

    def __copy__(self):
        return type(self)(self)

    def __repr__(self):
        return '%s(%s)' % (self._class_name, self._format_string)

    def __str__(self):
        return '{%s}' % self._format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        intervals = list(self.melodic_chromatic_intervals)
        intervals.sort(key=lambda x: x.number)
        return ', '.join([str(x) for x in intervals])

    ### PUBLIC PROPERTIES ###

    @property
    def harmonic_chromatic_interval_set(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedHarmonicIntervalSet(self)

    @property
    def melodic_chromatic_interval_numbers(self):
        return set([interval.number for interval in self])

    @property
    def melodic_chromatic_intervals(self):
        return set(self)
