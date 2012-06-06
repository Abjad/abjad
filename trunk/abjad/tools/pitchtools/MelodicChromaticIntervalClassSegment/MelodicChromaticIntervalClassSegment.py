from abjad.tools.pitchtools.IntervalClassObjectSegment import IntervalClassObjectSegment


class MelodicChromaticIntervalClassSegment(IntervalClassObjectSegment):
    '''.. versionadded:: 2.0

    Abjad model of melodic chromatic interval-class segment::

        >>> pitchtools.MelodicChromaticIntervalClassSegment([-2, -14, 3, 5.5, 6.5])
        MelodicChromaticIntervalClassSegment(-2, -2, +3, +5.5, +6.5)

    Melodic chromatic interval-class segments are immutable.
    '''

    def __new__(self, mcic_tokens):
        from abjad.tools import pitchtools
        mcics = []
        for mcic_token in mcic_tokens:
            mcic = pitchtools.MelodicChromaticIntervalClass(mcic_token)
            mcics.append(mcic)
        return tuple.__new__(self, mcics)
