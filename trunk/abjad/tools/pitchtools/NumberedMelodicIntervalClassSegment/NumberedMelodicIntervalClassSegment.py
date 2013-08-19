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

    def __new__(self, mcic_tokens):
        from abjad.tools import pitchtools
        mcics = []
        for mcic_token in mcic_tokens:
            mcic = pitchtools.NumberedMelodicIntervalClass(mcic_token)
            mcics.append(mcic)
        return tuple.__new__(self, mcics)
