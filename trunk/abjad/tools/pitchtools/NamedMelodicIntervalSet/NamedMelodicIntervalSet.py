# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.Set import Set


class NamedMelodicIntervalSet(Set):
    '''Abjad model of melodic diatonic interval set:

    ::

        >>> pitchtools.NamedMelodicIntervalSet('M2 M2 -m3 -P4')
        NamedMelodicIntervalSet('-P4 -m3 +M2')

    Melodic diatonic interval sets are immutable.
    '''

    ### CONSTRUCTOR ###

    def __new__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, str):
            interval_tokens = arg.split()
        else:
            interval_tokens = arg
        mdis = [pitchtools.NamedMelodicInterval(x) 
            for x in interval_tokens]
        return frozenset.__new__(self, mdis)

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
        return ' '.join(str(x) for x in sorted(self, key=lambda x: x.number))

