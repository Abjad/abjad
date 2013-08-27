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

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools 
        IntervalClassSet.__init__(
            self,
            tokens=tokens,
            item_class=pitchtools.NumberedInversionEquivalentIntervalClass,
            name=name,
            )

    ### SPECIAL METHODS ###

    def __copy__(self):
        return type(self)(self.numbers)

    def __repr__(self):
        return '%s(%s)' % (self._class_name, self._format_string)

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return ', '.join(str(x) for x in sorted(self, key=lambda x: x.number))

