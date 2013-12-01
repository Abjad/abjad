# -*- encoding: utf-8 -*-
import numbers
from abjad.tools import mathtools
from abjad.tools.pitchtools.IntervalClass import IntervalClass


class NumberedIntervalClass(IntervalClass):
    '''A numbered interval-class.

    ::

        >>> pitchtools.NumberedIntervalClass(-14)
        NumberedIntervalClass(-2)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    ### INITIALIZER ###

    def __init__(self, token=None):
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
        elif token is None:
            number = 0
        else:
            message = 'can not initialize {}: {!r}.'
            message = message.format(type(self).__name__, token)
            raise ValueError(message)
        self._number = number

    ### SPECIAL METHODS ###

    def __abs__(self):
        r'''Absolute value of numbered interval-class.

        Returns new numbered interval-class.
        '''
        return type(self)(abs(self._number))

    def __eq__(self, arg):
        r'''True when `arg` is a numbered interval-class with number equal to
        that of this numbered interval-class. Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    def __float__(self):
        r'''Changes numbered interval-class to float.

        Returns float.
        '''
        return float(self._number)

    def __int__(self):
        r'''Changes numbered interval-class to integer.

        Returns integer.
        '''
        return self._number

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return '{}{}'.format(self.direction_symbol, abs(self.number))

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = (
            self.number,
            )
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=(),
            positional_argument_values=positional_argument_values,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(cls, pitch_carrier_1, pitch_carrier_2):
        '''Makes numbered interval-class from `pitch_carrier_1` and
        `pitch_carrier_2`.

        ::

            >>> pitchtools.NumberedIntervalClass.from_pitch_carriers(
            ...     NamedPitch(-2), 
            ...     NamedPitch(12),
            ...     )
            NumberedIntervalClass(2)

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
        r'''Direction number of numbered interval-class.

        Returns -1, 0 or 1.
        '''
        if self.number < 1:
            return -1
        elif self.number == 1:
            return 0
        else:
            return 1

    @property
    def direction_symbol(self):
        r'''Direction symbol of numbered interval class.

        Returns string.
        '''
        if self.number < 1:
            return '-'
        else:
            return '+'

    @property
    def direction_word(self):
        r'''Direction word of numbered interval-class.

        Returns string.
        '''
        if self.number < 1:
            return 'descending'
        elif self.number == 1:
            return ''
        else:
            return 'ascending'
