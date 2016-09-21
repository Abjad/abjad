# -*- coding: utf-8 -*-
import numbers
from abjad.tools import mathtools
from abjad.tools.pitchtools.IntervalClass import IntervalClass


class NumberedIntervalClass(IntervalClass):
    '''Numbered interval-class.

    ..  container:: example

        **Example 1.** Initializes from integer:

        ::

            >>> pitchtools.NumberedIntervalClass(-14)
            NumberedIntervalClass(-2)

    ..  container:: example

        **Example 2.** Initializes from float:

        ::

            >>> pitchtools.NumberedIntervalClass(-14.5)
            NumberedIntervalClass(-2.5)

    ..  container:: example

        **Example 3.** Initializes from string:

        ::

            >>> pitchtools.NumberedIntervalClass('-14.5')
            NumberedIntervalClass(-2.5)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    ### INITIALIZER ###

    def __init__(self, item=None):
        from abjad.tools import pitchtools
        if isinstance(item, numbers.Number):
            sign = mathtools.sign(item)
            abs_token = abs(item)
            if abs_token % 12 == 0 and 12 <= abs_token:
                number = 12
            else:
                number = abs_token % 12
            number *= sign
        elif isinstance(item, pitchtools.Interval):
            number = item.semitones
            sign = mathtools.sign(number)
            abs_number = abs(number)
            if abs_number % 12 == 0 and 12 <= abs_number:
                number = 12
            else:
                number = abs_number % 12
            number *= sign
        elif isinstance(item, pitchtools.IntervalClass):
            number = item.number
            sign = mathtools.sign(number)
            abs_number = abs(number)
            if abs_number % 12 == 0 and 12 <= abs_number:
                number = 12
            else:
                number = abs_number % 12
            number *= sign
        elif item is None:
            number = 0
        elif isinstance(item, str):
            number = float(item)
            if mathtools.is_integer_equivalent_expr(number):
                number = int(number)
            sign = mathtools.sign(number)
            abs_token = abs(number)
            if abs_token % 12 == 0 and 12 <= abs_token:
                number = 12
            else:
                number = abs_token % 12
            number *= sign
        else:
            message = 'can not initialize {}: {!r}.'
            message = message.format(type(self).__name__, item)
            raise ValueError(message)
        self._number = number

    ### SPECIAL METHODS ###

    def __abs__(self):
        r'''Absolute value of numbered interval-class.

        Returns new numbered interval-class.
        '''
        return type(self)(abs(self._number))

    def __eq__(self, arg):
        r'''Is true when `arg` is a numbered interval-class with number equal to
        that of this numbered interval-class. Otherwise false.

        Returns true or false.
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

    def __hash__(self):
        r'''Hashes numbered interval-class.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(NumberedIntervalClass, self).__hash__()

    def __int__(self):
        r'''Changes numbered interval-class to integer.

        Returns integer.
        '''
        return self._number

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(class_, pitch_carrier_1, pitch_carrier_2):
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
        return class_(interval)

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return '{}{}'.format(self.direction_symbol, abs(self.number))

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
