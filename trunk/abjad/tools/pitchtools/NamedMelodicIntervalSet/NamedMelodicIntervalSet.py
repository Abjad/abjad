# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.IntervalSet import IntervalSet


class NamedMelodicIntervalSet(IntervalSet):
    '''Abjad model of melodic diatonic interval set:

    ::

        >>> pitchtools.NamedMelodicIntervalSet('M2 M2 -m3 -P4')
        NamedMelodicIntervalSet('-P4 -m3 +M2')

    Melodic diatonic interval sets are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools 
        IntervalSet.__init__(
            self,
            tokens=tokens,
            item_class=pitchtools.NamedMelodicInterval,
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
        return ' '.join(str(x) for x in sorted(self, key=lambda x: x.number))

