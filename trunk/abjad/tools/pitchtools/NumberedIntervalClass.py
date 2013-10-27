# -*- encoding: utf-8 -*-
import numbers
from abjad.tools import mathtools
from abjad.tools.pitchtools.IntervalClass import IntervalClass


class NumberedIntervalClass(IntervalClass):
    '''A numbered interval-class.

    ::

        >>> pitchtools.NumberedIntervalClass(-14)
        NumberedIntervalClass(-2)

    Returns numbered interval-class.
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

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return '%s%s' % (self.direction_symbol, abs(self.number))

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(cls, pitch_carrier_1, pitch_carrier_2):
        '''Calculate numbered interval-class from `pitch_carrier_1` to
        `pitch_carrier_2`:

        ::

            >>> pitchtools.NumberedIntervalClass.from_pitch_carriers(
            ...     pitchtools.NamedPitch(-2), 
            ...     pitchtools.NamedPitch(12),
            ...     )
            NumberedIntervalClass(+2)

        Returns numbered interval-class.
        '''
        from abjad.tools import pitchtools
        # get numbered interval
        interval = pitchtools.NumberedInterval.from_pitch_carriers(
            pitch_carrier_1, pitch_carrier_2)
        # return numbered interval-class
        return cls(interval)

    ### PUBLIC PROPERTIES ###

    @property
    def direction_number(self):
        if self.number < 1:
            return -1
        elif self.number == 1:
            return 0
        else:
            return 1

    @property
    def direction_symbol(self):
        if self.number < 1:
            return '-'
        else:
            return '+'

    @property
    def direction_word(self):
        if self.number < 1:
            return 'descending'
        elif self.number == 1:
            return ''
        else:
            return 'ascending'
