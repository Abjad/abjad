# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.Set import Set


class NamedHarmonicIntervalSet(Set):
    '''Abjad model of harmonic diatonic interval set:

    ::

        >>> pitchtools.NamedHarmonicIntervalSet('m2 m2 M2 M9')
        NamedHarmonicIntervalSet('m2 M2 M9')

    Harmonic diatonic interval sets are immutable.
    '''

    ### CONSTRUCTOR ###

    def __new__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, str):
            interval_tokens = arg.split()
        else:
            interval_tokens = arg
        hdis = [pitchtools.NamedHarmonicInterval(x) 
            for x in interval_tokens]
        return frozenset.__new__(self, hdis)

    ### SPECIAL METHODS ###

    def __copy__(self):
        return type(self)(self)

    def __repr__(self):
        return "%s('%s')" % (self._class_name, self._format_string)

    def __str__(self):
        return '{%s}' % self._format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return ' '.join([str(x) for x in 
            sorted(self)])

