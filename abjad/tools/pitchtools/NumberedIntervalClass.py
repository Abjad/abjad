import numbers
from abjad.tools import mathtools
from abjad.tools.pitchtools.IntervalClass import IntervalClass


class NumberedIntervalClass(IntervalClass):
    '''Numbered interval-class.

    ..  container:: example

        Initializes from integer:

        >>> abjad.NumberedIntervalClass(-14)
        NumberedIntervalClass(-2)

    ..  container:: example

        Initializes from float:

        >>> abjad.NumberedIntervalClass(-14.5)
        NumberedIntervalClass(-2.5)

    ..  container:: example

        Initializes from string:

        >>> abjad.NumberedIntervalClass('-14.5')
        NumberedIntervalClass(-2.5)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    ### INITIALIZER ###

    def __init__(self, number=0):
        from abjad.tools import pitchtools
        if isinstance(number, numbers.Number):
            sign = mathtools.sign(number)
            abs_token = abs(number)
            if abs_token % 12 == 0 and 12 <= abs_token:
                number = 12
            else:
                number = abs_token % 12
            number *= sign
        elif isinstance(number, pitchtools.Interval):
            number = number.semitones
            sign = mathtools.sign(number)
            abs_number = abs(number)
            if abs_number % 12 == 0 and 12 <= abs_number:
                number = 12
            else:
                number = abs_number % 12
            number *= sign
        elif isinstance(number, pitchtools.IntervalClass):
            number = number.number
            sign = mathtools.sign(number)
            abs_number = abs(number)
            if abs_number % 12 == 0 and 12 <= abs_number:
                number = 12
            else:
                number = abs_number % 12
            number *= sign
        elif isinstance(number, str):
            number = float(number)
            if mathtools.is_integer_equivalent(number):
                number = int(number)
            sign = mathtools.sign(number)
            abs_token = abs(number)
            if abs_token % 12 == 0 and 12 <= abs_token:
                number = 12
            else:
                number = abs_token % 12
            number *= sign
        else:
            message = 'can not initialize {} from {!r}.'
            message = message.format(type(self).__name__, number)
            raise ValueError(message)
        self._number = number

    ### SPECIAL METHODS ###

    def __abs__(self):
        r'''Gets absolute value of numbered interval-class.

        Returns new numbered interval-class.
        '''
        return type(self)(abs(self.number))

    def __eq__(self, argument):
        r'''Is true when `argument` is a numbered interval-class with number
        equal to that of this numbered interval-class. Otherwise false.

        ..  container:: example

            >>> interval_class_1 = abjad.NumberedIntervalClass(0)
            >>> interval_class_2 = abjad.NumberedIntervalClass(0)
            >>> interval_class_3 = abjad.NumberedIntervalClass(1)

            >>> interval_class_1 == interval_class_1
            True
            >>> interval_class_1 == interval_class_2
            True
            >>> interval_class_1 == interval_class_3
            False

            >>> interval_class_2 == interval_class_1
            True
            >>> interval_class_2 == interval_class_2
            True
            >>> interval_class_2 == interval_class_3
            False

            >>> interval_class_3 == interval_class_1
            False
            >>> interval_class_3 == interval_class_2
            False
            >>> interval_class_3 == interval_class_3
            True

        Returns true or false.
        '''
        return super(NumberedIntervalClass, self).__eq__(argument)

    def __hash__(self):
        r'''Hashes numbered interval-class.

        Returns integer.
        '''
        return super(NumberedIntervalClass, self).__hash__()

    def __lt__(self, argument):
        r'''Is true when numbered interval-class is less than `argument`.

        ..  container:: example

            >>> interval_class_1 = abjad.NumberedIntervalClass(0)
            >>> interval_class_2 = abjad.NumberedIntervalClass(0)
            >>> interval_class_3 = abjad.NumberedIntervalClass(1)

            >>> interval_class_1 < interval_class_1
            False
            >>> interval_class_1 < interval_class_2
            False
            >>> interval_class_1 < interval_class_3
            True

            >>> interval_class_2 < interval_class_1
            False
            >>> interval_class_2 < interval_class_2
            False
            >>> interval_class_2 < interval_class_3
            True

            >>> interval_class_3 < interval_class_1
            False
            >>> interval_class_3 < interval_class_2
            False
            >>> interval_class_3 < interval_class_3
            False

        Returns true or false.
        '''
        try:
            argument = type(self)(argument)
        except:
            return False
        return self.number < argument.number

    def __str__(self):
        r'''Gets string representation of numbered interval-class.

        ..  container:: example

            >>> str(abjad.NumberedIntervalClass(-13))
            '-1'

            >>> str(abjad.NumberedIntervalClass(0))
            '0'

            >>> str(abjad.NumberedIntervalClass(13))
            '+1'

        '''
        string = super(NumberedIntervalClass, self).__str__()
        if 0 < self.number:
            string = '+' + string
        return string

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        return abjad.FormatSpecification(
            client=self,
            coerce_for_equality=True,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=[self.number],
            )

    ### PUBLIC PROPERTIES ###

    @property
    def direction_number(self):
        r'''Gets direction number of numbered interval-class.

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
        r'''Gets direction symbol of numbered interval-class.

        Returns string.
        '''
        if self.number < 1:
            return '-'
        else:
            return '+'

    @property
    def direction_word(self):
        r'''Gets direction word of numbered interval-class.

        Returns string.
        '''
        if self.number < 1:
            return 'descending'
        elif self.number == 1:
            return ''
        else:
            return 'ascending'

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(class_, pitch_carrier_1, pitch_carrier_2):
        '''Makes numbered interval-class from `pitch_carrier_1` and
        `pitch_carrier_2`.

        ..  container:: example

            >>> abjad.NumberedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(-2),
            ...     abjad.NamedPitch(12),
            ...     )
            NumberedIntervalClass(2)

            >>> abjad.NumberedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(0),
            ...     abjad.NamedPitch(12),
            ...     )
            NumberedIntervalClass(12)

            >>> abjad.NumberedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(9),
            ...     abjad.NamedPitch(12),
            ...     )
            NumberedIntervalClass(3)

            >>> abjad.NumberedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(9),
            ...     )
            NumberedIntervalClass(-3)

            >>> abjad.NumberedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(12),
            ...     )
            NumberedIntervalClass(0)

            >>> abjad.NumberedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(-2),
            ...     )
            NumberedIntervalClass(-2)

        Returns numbered interval-class.
        '''
        from abjad.tools import pitchtools
        interval = pitchtools.NumberedInterval.from_pitch_carriers(
            pitch_carrier_1,
            pitch_carrier_2,
            )
        return class_(interval)
