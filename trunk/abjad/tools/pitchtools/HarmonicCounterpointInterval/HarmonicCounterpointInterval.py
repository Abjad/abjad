# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.CounterpointInterval import CounterpointInterval


class HarmonicCounterpointInterval(CounterpointInterval):
    '''Abjad model of harmonic counterpoint interval:

    ::

        >>> pitchtools.HarmonicCounterpointInterval(-9)
        HarmonicCounterpointInterval(9)

    Harmonic counterpoint intervals are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, token):
        from abjad.tools import pitchtools
        if isinstance(token, int):
            _number = abs(token)
        elif isinstance(token, pitchtools.NamedInterval):
            _number = abs(token.number)
        else:
            raise TypeError('must be number or diatonic interval.')
        object.__setattr__(self, '_number', _number)

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    def __ne__(self, arg):
        return not self == arg

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(cls, pitch_carrier_1, pitch_carrier_2):
        '''Calculate harmonic counterpoint interval `pitch_carrier_1` to
        `pitch_carrier_2`:

        ::

            >>> pitchtools.HarmonicCounterpointInterval.from_pitch_carriers(
            ...     pitchtools.NamedChromaticPitch(-2), 
            ...     pitchtools.NamedChromaticPitch(12),
            ...     )
            HarmonicCounterpointInterval(9)

        Return harmonic counterpoint interval-class.
        '''
        from abjad.tools import pitchtools
        # get melodic diatonic interval
        mdi = pitchtools.MelodicDiatonicInterval.from_pitch_carriers(
            pitch_carrier_1, pitch_carrier_2)
        # return harmonic counterpoint interval
        return mdi.harmonic_counterpoint_interval

    ### PUBLIC PROPERTIES ###

    @property
    def harmonic_counterpoint_interval_class(self):
        from abjad.tools import pitchtools
        return pitchtools.HarmonicCounterpointIntervalClass(self)
