# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.IntervalSegment import IntervalSegment


class NamedMelodicIntervalSegment(IntervalSegment):
    '''Abjad model of melodic diatonic interval segment:

    ::

        >>> pitchtools.NamedMelodicIntervalSegment('M2 M9 -m3 -P4')
        NamedMelodicIntervalSegment('+M2 +M9 -m3 -P4')

    Melodic diatonic interval segments are immutable.
    '''

    ### CONSTRUCTOR ###

    def __new__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, str):
            melodic_diatonic_interval_tokens = arg.split()
        else:
            melodic_diatonic_interval_tokens = arg
        mdis = []
        for token in melodic_diatonic_interval_tokens:
            mdi = pitchtools.NamedMelodicInterval(token)
            mdis.append(mdi)
        return tuple.__new__(self, mdis)

    ### SPECIAL METHODS ###

    def __copy__(self):
        return type(self)(self.intervals)

    def __repr__(self):
        return "%s('%s')" % (
            self._class_name, ' '.join([str(x) for x in self]))

    ### PUBLIC PROPERTIES ###

    @property
    def harmonic_chromatic_interval_segment(self):
        from abjad.tools import pitchtools
        return pitchtools.HarmonicChromaticIntervalSegment(self.intervals)

    @property
    def harmonic_diatonic_interval_segment(self):
        from abjad.tools import pitchtools
        return pitchtools.HarmonicDiatonicIntervalSegment(self.intervals)

    @property
    def melodic_chromatic_interval_segment(self):
        from abjad.tools import pitchtools
        return pitchtools.MelodicChromaticIntervalSegment(self.intervals)
