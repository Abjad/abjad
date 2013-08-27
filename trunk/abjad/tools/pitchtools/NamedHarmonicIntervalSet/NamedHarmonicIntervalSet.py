# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.IntervalSet import IntervalSet


class NamedHarmonicIntervalSet(IntervalSet):
    '''Abjad model of harmonic diatonic interval set:

    ::

        >>> pitchtools.NamedHarmonicIntervalSet('m2 m2 M2 M9')
        NamedHarmonicIntervalSet('m2 M2 M9')

    Harmonic diatonic interval sets are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools 
        IntervalSet.__init__(
            self,
            tokens=tokens,
            item_class=pitchtools.NamedHarmonicInterval,
            name=name,
            )

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

