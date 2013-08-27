# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.IntervalSegment import IntervalSegment


class NamedHarmonicIntervalSegment(IntervalSegment):
    '''Abjad model of harmonic diatonic interval segment:

    ::

        >>> pitchtools.NamedHarmonicIntervalSegment('m2 M9 m3 M3')
        NamedHarmonicIntervalSegment('m2 M9 m3 M3')

    Harmonic diatonic interval segments are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools
        IntervalSegment.__init__(
            self,
            tokens=tokens,
            item_class=pitchtools.NamedHarmonicInterval,
            name=None,
            )

    ### SPECIAL METHODS ###

    def __copy__(self):
        return type(self)(self.intervals)

    def __repr__(self):
        return "%s('%s')" % (
            self._class_name, ' '.join([str(x) for x in self]))

