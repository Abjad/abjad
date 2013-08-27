# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.IntervalClassSegment import IntervalClassSegment


class NumberedMelodicIntervalClassSegment(IntervalClassSegment):
    '''Abjad model of melodic chromatic interval-class segment:

    ::

        >>> pitchtools.NumberedMelodicIntervalClassSegment(
        ...     [-2, -14, 3, 5.5, 6.5])
        NumberedMelodicIntervalClassSegment(-2, -2, +3, +5.5, +6.5)

    Melodic chromatic interval-class segments are immutable.
    '''

    ### CONSTRUCTOR ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools
        IntervalClassSegment.__init__(
            self,
            tokens=tokens,
            item_class=pitchtools.NumberedMelodicIntervalClass,
            name=None,
            )
