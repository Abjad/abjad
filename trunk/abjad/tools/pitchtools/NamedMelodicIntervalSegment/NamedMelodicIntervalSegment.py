# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.IntervalSegment import IntervalSegment


class NamedMelodicIntervalSegment(IntervalSegment):
    '''Abjad model of melodic diatonic interval segment:

    ::

        >>> pitchtools.NamedMelodicIntervalSegment('M2 M9 -m3 -P4')
        NamedMelodicIntervalSegment('+M2 +M9 -m3 -P4')

    Melodic diatonic interval segments are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools
        IntervalSegment.__init__(
            self,
            tokens=tokens,
            item_class=pitchtools.NamedMelodicInterval,
            name=None,
            )

    ### SPECIAL METHODS ###

    def __copy__(self):
        return type(self)(self.intervals)

    def __repr__(self):
        return "%s('%s')" % (
            self._class_name, ' '.join([str(x) for x in self]))

