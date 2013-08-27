# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.IntervalSet import IntervalSet


class NumberedHarmonicIntervalSet(IntervalSet):
    '''Abjad model of harmonic chromatic interval set:

    ::

        >>> pitchtools.NumberedHarmonicIntervalSet([10, -12, -13, -13, -13.5])
        NumberedHarmonicIntervalSet(10, 12, 13, 13.5)

    Harmonic chromatic interval sets are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools 
        IntervalSet.__init__(
            self,
            tokens=tokens,
            item_class=pitchtools.NumberedHarmonicInterval,
            name=name,
            )

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
        return ', '.join([str(x) for x in sorted(
            self.harmonic_chromatic_intervals)])

    ### PUBLIC PROPERTIES ###

    @property
    def harmonic_chromatic_interval_numbers(self):
        return set([interval.number for interval in self])

    @property
    def harmonic_chromatic_intervals(self):
        return set(self)
