# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.IntervalClassSet import IntervalClassSet


class NumberedInversionEquivalentIntervalClassSet(IntervalClassSet):
    '''Abjad model of inversion-equivalent chromatic interval-class set:

    ::

        >>> pitchtools.NumberedInversionEquivalentIntervalClassSet(
        ...     [1, 1, 6, 2, 2])
        NumberedInversionEquivalentIntervalClassSet(1, 2, 6)

    Inversion-equivalent chromatic interval-class sets are immutable.
    '''

    ### CONSTRUCTOR ###

    def __new__(self, interval_class_tokens):
        from abjad.tools import pitchtools
        iecics = []
        for token in interval_class_tokens:
            iecic = pitchtools.NumberedInversionEquivalentIntervalClass(token)
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
        return ', '.join(str(x) for x in sorted(self, key=lambda x: x.number))

