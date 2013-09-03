# -*- encoding: utf-8 -*-
import numbers
from abjad.tools.pitchtools.NumberedIntervalClass import NumberedIntervalClass


class NumberedHarmonicIntervalClass(NumberedIntervalClass):
    '''Abjad model of harmonic chromatic interval-class:

    ::

        >>> pitchtools.NumberedHarmonicIntervalClass(-14)
        NumberedHarmonicIntervalClass(2)

    Harmonic chromatic interval-classes are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, token):
        from abjad.tools import pitchtools
        if isinstance(token, numbers.Number):
            number = token
        elif isinstance(token, pitchtools.Interval):
            number = token.semitones
        else:
            raise TypeError('must be number or interval instance.')
        if number % 12 == 0 and 12 <= abs(number):
            number = 12
        else:
            number = abs(number) % 12
        self._number = number

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
        '''Calculate harmonic chromatic interval-class from `pitch_carrier_1` to
        `pitch_carrier_2`:

        ::

            >>> pitchtools.NumberedHarmonicIntervalClass.from_pitch_carriers(
            ... pitchtools.NamedPitch(-2), pitchtools.NamedPitch(12))
            NumberedHarmonicIntervalClass(2)

        Return harmonic chromatic interval-class.
        '''
        from abjad.tools import pitchtools
        # get melodic chromatic interval
        interval = pitchtools.NumberedMelodicInterval.from_pitch_carriers(
            pitch_carrier_1, pitch_carrier_2)
        # return harmonic chromatic interval-class
        return cls(interval)
