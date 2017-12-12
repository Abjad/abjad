from abjad.tools import mathtools
from abjad.tools.pitchtools.IntervalClass import IntervalClass


class NamedIntervalClass(IntervalClass):
    '''Named interval-class.

    ..  container:: example

        Initializes from name:

        >>> abjad.NamedIntervalClass('-M9')
        NamedIntervalClass('-M2')


    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        '_quality_string',
        )

    _acceptable_quality_strings = (
        'perfect',
        'major',
        'minor',
        'diminished',
        'augmented',
        )

    _interval_number_to_interval_string = {
        1: 'unison',
        2: 'second',
        3: 'third',
        4: 'fourth',
        5: 'fifth',
        6: 'sixth',
        7: 'seventh',
        8: 'octave',
        }

    _quality_abbreviation_to_quality_string = {
        'M': 'major',
        'm': 'minor',
        'P': 'perfect',
        'aug': 'augmented',
        'dim': 'diminished',
        }

    _quality_string_to_quality_abbreviation = {
        'major': 'M',
        'minor': 'm',
        'perfect': 'P',
        'augmented': 'aug',
        'diminished': 'dim',
        }

    ### INITIALIZER ###

    def __init__(self, name='P1'):
        from abjad.tools import pitchtools
        named_prototype = (pitchtools.NamedInterval, type(self))
        if isinstance(name, str):
            class_ = pitchtools.Interval
            match = class_._interval_name_abbreviation_regex.match(name)
            if match is None:
                message = 'can not initialize {} from {!r}.'
                message = message.format(type(self).__name__, name)
                raise ValueError(message)
            result = match.groups()
            direction_string, quality_abbreviation, number_string = result
            class_ = type(self)
            quality_string = class_._quality_abbreviation_to_quality_string[
                quality_abbreviation
                ]
            number = int(direction_string + number_string)
        elif isinstance(name, named_prototype):
            quality_string = name._quality_string
            number = name.number
        elif isinstance(name, tuple) and len(name) == 2:
            quality_string, number = name
        else:
            message = 'can not initialize {} from {!r}.'
            message = message.format(type(self).__name__, name)
            raise TypeError(message)
        if quality_string not in type(self)._acceptable_quality_strings:
            raise Exception(repr(quality_string))
        assert isinstance(number, int), repr(number)
        if number == 0:
            message = 'must be nonzero: {!r}.'
            message = message.format(number)
            raise ValueError(number)
        sign = mathtools.sign(number)
        abs_number = abs(number)
        if abs_number % 7 == 1 and 8 <= abs_number:
            number = 8
        else:
            number = abs_number % 7
            if number == 0:
                number = 7
        if not number == 1:
            number *= sign
        self._number = number
        self._quality_string = quality_string

    ### SPECIAL METHODS ###

    def __abs__(self):
        r'''Gets absolute value of named interval-class.

        ..  container:: example

            >>> abs(abjad.NamedIntervalClass('-M9'))
            NamedIntervalClass('+M2')

        Returns new named interval-class.
        '''
        return type(self).from_quality_and_number(
            self.quality_string,
            abs(self.number),
            )

    def __eq__(self, argument):
        r'''Is true when `argument` is a named interval-class with direction
        number, quality string and number equal to those of this named
        interval-class. Otherwise false.

        ..  container:: example

            >>> interval_class_1 = abjad.NamedIntervalClass('P1')
            >>> interval_class_2 = abjad.NamedIntervalClass('P1')
            >>> interval_class_3 = abjad.NamedIntervalClass('m2')

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
        return super(NamedIntervalClass, self).__eq__(argument)

    def __float__(self):
        r'''Coerce to float.

        Returns float.
        '''
        return float(self.number)

    def __hash__(self):
        r'''Hashes named interval-class.

        Returns integer.
        '''
        return super(NamedIntervalClass, self).__hash__()

    def __lt__(self, argument):
        r'''Is true when `argument` is a named interval class with a number
        greater than that of this named interval.

        ..  container:: example

            >>> interval_class_1 = abjad.NamedIntervalClass('P1')
            >>> interval_class_2 = abjad.NamedIntervalClass('P1')
            >>> interval_class_3 = abjad.NamedIntervalClass('m2')

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
        import abjad
        try:
            argument = type(self)(argument)
        except:
            return False
        if self.number == argument.number:
            self_semitones = abjad.NamedInterval(self).semitones
            argument_semitones = abjad.NamedInterval(argument).semitones
            return self_semitones < argument_semitones
        return self.number < argument.number

    def __str__(self):
        r'''Gets string representation of named interval-class.

        ..  container:: example

            >>> str(abjad.NamedIntervalClass('-M9'))
            '-M2'

        Returns string.
        '''
        return self.name

    ### PRIVATE PROPERTIES ###

    @property
    def _full_name(self):
        strings = []
        if self.direction_string:
            strings.append(self.direction_string)
        strings.extend([self._quality_string, self._interval_string])
        return ' '.join(strings)

    @property
    def _interval_string(self):
        return self._interval_number_to_interval_string[abs(self.number)]

    @property
    def _quality_abbreviation(self):
        return self._quality_string_to_quality_abbreviation[
            self._quality_string]

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        values = [self.name]
        return abjad.FormatSpecification(
            client=self,
            coerce_for_equality=True,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def direction_number(self):
        r'''Gets direction number of named interval-class.

        ..  container:: example

            >>> abjad.NamedIntervalClass('P1').direction_number
            0

            >>> abjad.NamedIntervalClass('+M2').direction_number
            1

            >>> abjad.NamedIntervalClass('-M2').direction_number
            -1

        Returns -1, 0 or 1.
        '''
        if self.number < 1:
            return -1
        elif self.number == 1:
            return 0
        else:
            return 1

    @property
    def direction_string(self):
        r'''Gets direction string of named interval-class.

        ..  container:: example

            >>> abjad.NamedIntervalClass('P1').direction_string is None
            True

            >>> abjad.NamedIntervalClass('+M2').direction_string
            'ascending'

            >>> abjad.NamedIntervalClass('-M2').direction_string
            'descending'

        Returns string.
        '''
        if self.direction_number == -1:
            return 'descending'
        elif self.direction_number == 0:
            return None
        elif self.direction_number == 1:
            return 'ascending'

    @property
    def direction_symbol(self):
        r'''Gets direction symbol of named interval-class.

        ..  container:: example

            >>> abjad.NamedIntervalClass('P1').direction_symbol
            ''

            >>> abjad.NamedIntervalClass('+M2').direction_symbol
            '+'

            >>> abjad.NamedIntervalClass('-M2').direction_symbol
            '-'

        Returns string.
        '''
        if self.number < 1:
            return '-'
        elif self.number == 1:
            return ''
        else:
            return '+'

    @property
    def name(self):
        r'''Gets name of named interval-class.

        ..  container:: example

            >>> abjad.NamedIntervalClass('-M9').name
            '-M2'

        Returns string.
        '''
        return '{}{}{}'.format(
            self.direction_symbol,
            self._quality_abbreviation,
            abs(self.number),
            )

    @property
    def quality_string(self):
        r'''Gets quality string of named interval-class.

        ..  container:: example

            >>> abjad.NamedIntervalClass('P1').quality_string
            'perfect'

            >>> abjad.NamedIntervalClass('+M2').quality_string
            'major'

            >>> abjad.NamedIntervalClass('-M2').quality_string
            'major'

        Returns string.
        '''
        return self._quality_string

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(class_, pitch_carrier_1, pitch_carrier_2):
        '''Makes named interval-class from `pitch_carrier_1` and
        `pitch_carrier_2`.

        ..  container:: example

            >>> abjad.NamedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(-2),
            ...     abjad.NamedPitch(12),
            ...     )
            NamedIntervalClass('+M2')

        ..  container:: example

            >>> abjad.NamedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(0),
            ...     abjad.NamedPitch(12),
            ...     )
            NamedIntervalClass('+P8')

        ..  container:: example

            >>> abjad.NamedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(12),
            ...     )
            NamedIntervalClass('P1')

        ..  container:: example

            >>> abjad.NamedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(-3),
            ...     )
            NamedIntervalClass('-m3')

        ..  container:: example

            >>> abjad.NamedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(9),
            ...     )
            NamedIntervalClass('-m3')

        Returns newly constructed named interval-class.
        '''
        from abjad.tools import pitchtools
        named_interval = pitchtools.NamedInterval.from_pitch_carriers(
            pitch_carrier_1,
            pitch_carrier_2,
            )
        return class_(named_interval)

    @classmethod
    def from_quality_and_number(class_, quality, number):
        r'''Makes named interval-class from `quality` string and number.

        ..  container:: example

            >>> abjad.NamedIntervalClass.from_quality_and_number(
            ...     'major',
            ...     -9,
            ...     )
            NamedIntervalClass('-M2')

        Returns newly constructed named interval-class.
        '''
        name = NamedIntervalClass.quality_and_number_to_name(quality, number)
        interval_class = class_(name)
        return interval_class

    @staticmethod
    def quality_and_number_to_name(quality, number):
        r'''Changes `quality` and `number` to name.

        ..  container:: example

            >>> class_ = abjad.NamedIntervalClass
            >>> class_.quality_and_number_to_name('minor', 2)
            '+m2'
            >>> class_.quality_and_number_to_name('major', 2)
            '+M2'
            >>> class_.quality_and_number_to_name('minor', 3)
            '+m3'
            >>> class_.quality_and_number_to_name('major', 3)
            '+M3'

        Returns string.
        '''
        class_ = NamedIntervalClass
        abbreviation = class_._quality_string_to_quality_abbreviation[
            quality]
        if number == 1:
            direction = ''
        elif mathtools.sign(number) == 1:
            direction = '+'
        else:
            direction = '-'
        sign = mathtools.sign(number)
        abs_number = abs(number)
        if abs_number % 7 == 1 and 8 <= abs_number:
            number = 8
        else:
            number = abs_number % 7
            if number == 0:
                number = 7
        if not number == 1:
            number *= sign
        number = abs(number)
        string = '{}{}{}'.format(direction, abbreviation, number)
        return string
