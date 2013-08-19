# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.pitchtools.CounterpointIntervalClass \
	import CounterpointIntervalClass
from abjad.tools.pitchtools.MelodicIntervalClass import MelodicIntervalClass


class MelodicCounterpointIntervalClass(
    CounterpointIntervalClass, MelodicIntervalClass):
    '''Abjad model of melodic counterpoint interval-class:

    ::

        >>> pitchtools.MelodicCounterpointIntervalClass(-9)
        MelodicCounterpointIntervalClass(-2)

    Melodic counterpoint interval-classes are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    ### INITIALIZER ###

    def __init__(self, token):
        from abjad.tools import pitchtools
        if isinstance(token, int):
            number = token
        elif isinstance(token, pitchtools.CounterpointInterval):
            number = token.number
        if number == 0:
            raise ValueError('must be nonzero.')
        if abs(number) == 1:
            object.__setattr__(self, '_number', 1)
        else:
            sign = mathtools.sign(number)
            number = abs(number) % 7
            if number == 0:
                number = 7
            elif number == 1:
                number = 8
            number *= sign
            object.__setattr__(self, '_number', number)

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(cls, pitch_carrier_1, pitch_carrier_2):
        '''Calculate melodic counterpoint interval-class from `pitch_carrier_1` to
        `pitch_carrier_2`:

        ::

            >>> pitchtools.MelodicCounterpointIntervalClass.from_pitch_carriers(
            ...     pitchtools.NamedChromaticPitch(-2), 
            ...     pitchtools.NamedChromaticPitch(12),
            ...     )
            MelodicCounterpointIntervalClass(+2)

        Return melodic counterpoint interval-class.
        '''
        from abjad.tools import pitchtools
        # get melodic diatonic interval
        mdi = pitchtools.MelodicDiatonicInterval.from_pitch_carriers(
            pitch_carrier_1, pitch_carrier_2)
        # return melodic counterpoint interval-class
        return mdi.melodic_counterpoint_interval.melodic_counterpoint_interval_class
