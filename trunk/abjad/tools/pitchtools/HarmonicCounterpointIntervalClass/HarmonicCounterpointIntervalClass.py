# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.CounterpointIntervalClass \
	import CounterpointIntervalClass


class HarmonicCounterpointIntervalClass(CounterpointIntervalClass):
    '''Abjad model of harmonic counterpoint interval-class:

    ::

        >>> pitchtools.HarmonicCounterpointIntervalClass(-9)
        HarmonicCounterpointIntervalClass(2)

    Harmonic counterpoint interval-classes are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, token):
        from abjad.tools import pitchtools
        if isinstance(token, int):
            _number = token
        elif isinstance(token, (
            pitchtools.NamedInterval,
            pitchtools.CounterpointInterval)):
            _number = token.number
        if _number == 0:
            raise ValueError('must be nonzero.')
        if abs(_number) == 1:
            _number = 1
        else:
            _number = abs(_number) % 7
            if _number == 0:
                _number = 7
            elif _number == 1:
                _number = 8
        object.__setattr__(self, '_number', _number)

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(cls, pitch_carrier_1, pitch_carrier_2):
        '''Calculate harmonic counterpoint interval-class from `pitch_carrier_1` to
        `pitch_carrier_2`:

        ::

            >>> pitchtools.HarmonicCounterpointIntervalClass.from_pitch_carriers(
            ...     pitchtools.NamedChromaticPitch(-2), 
            ...     pitchtools.NamedChromaticPitch(12),
            ...     )
            HarmonicCounterpointIntervalClass(2)

        Return harmonic counterpoint interval-class.
        '''
        from abjad.tools import pitchtools

        # get melodic diatonic interval
        mdi = pitchtools.MelodicDiatonicInterval.from_pitch_carriers(
            pitch_carrier_1, pitch_carrier_2)

        # return harmonic counterpoint interval-class
        return mdi.harmonic_counterpoint_interval.harmonic_counterpoint_interval_class
