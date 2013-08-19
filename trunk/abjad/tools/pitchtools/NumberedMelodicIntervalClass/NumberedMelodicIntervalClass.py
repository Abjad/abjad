# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.pitchtools.MelodicIntervalClass import MelodicIntervalClass
from abjad.tools.pitchtools.NumberedIntervalClass import NumberedIntervalClass
import numbers


class NumberedMelodicIntervalClass(
    NumberedIntervalClass, MelodicIntervalClass):
    '''Abjad model of melodic chromatic interval-class:

    ::

        >>> pitchtools.NumberedMelodicIntervalClass(-14)
        NumberedMelodicIntervalClass(-2)

    Melodic chromatic interval-classes are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, token):
        from abjad.tools import pitchtools
        if isinstance(token, numbers.Number):
            sign = mathtools.sign(token)
            abs_token = abs(token)
            if abs_token % 12 == 0 and 12 <= abs_token:
                number = 12
            else:
                number = abs_token % 12
            number *= sign
        elif isinstance(token, pitchtools.Interval):
            number = token.semitones
            sign = mathtools.sign(number)
            abs_number = abs(number)
            if abs_number % 12 == 0 and 12 <= abs_number:
                number = 12
            else:
                number = abs_number % 12
            number *= sign
        elif isinstance(token, pitchtools.IntervalClass):
            number = token.number
            sign = mathtools.sign(number)
            abs_number = abs(number)
            if abs_number % 12 == 0 and 12 <= abs_number:
                number = 12
            else:
                number = abs_number % 12
            number *= sign
        else:
            raise ValueError('must be number, interval or interval-class.')
        object.__setattr__(self, '_number', number)

    ### SPECIAL METHODS ###

    def __abs__(self):
        return type(self)(abs(self._number))

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    def __float__(self):
        return float(self._number)

    def __int__(self):
        return self._number

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(cls, pitch_carrier_1, pitch_carrier_2):
        '''Calculate melodic chromatic interval-class from `pitch_carrier_1` to
        `pitch_carrier_2`:

        ::

            >>> pitchtools.NumberedMelodicIntervalClass.from_pitch_carriers(
            ...     pitchtools.NamedPitch(-2), 
            ...     pitchtools.NamedPitch(12),
            ...     )
            NumberedMelodicIntervalClass(+2)

        Return melodic chromatic interval-class.
        '''
        from abjad.tools import pitchtools
        # get melodic chromatic interval
        mci = pitchtools.NumberedMelodicInterval.from_pitch_carriers(
            pitch_carrier_1, pitch_carrier_2)
        # return melodic chromatic interval-class
        return mci.melodic_chromatic_interval_class
