# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.pitchtools.IntervalSegment import IntervalSegment


class NumberedMelodicIntervalSegment(IntervalSegment):
    '''Abjad model of melodic chromatic interval segment:

    ::

        >>> pitchtools.NumberedMelodicIntervalSegment(
        ...     [11, 13, 13.5, -2, 2.5])
        NumberedMelodicIntervalSegment([+11, +13, +13.5, -2, +2.5])

    Melodic chromatic interval segments are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools
        IntervalSegment.__init__(
            self,
            tokens=tokens,
            item_class=pitchtools.NumberedMelodicInterval,
            name=name,
            )

    ### SPECIAL METHODS ###

    def __copy__(self):
        return type(self)(self.intervals)

    ### PUBLIC PROPERTIES ###

