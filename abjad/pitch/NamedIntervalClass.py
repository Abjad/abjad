from abjad import mathtools
from abjad.pitch.IntervalClass import IntervalClass
from . import constants


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

    ### INITIALIZER ###

    def __init__(self, name='P1'):
        super().__init__(name or 'P1')

    ### SPECIAL METHODS ###

    def __abs__(self):
        r'''Gets absolute value of named interval-class.

        ..  container:: example

            >>> abs(abjad.NamedIntervalClass('-M9'))
            NamedIntervalClass('+M2')

        Returns new named interval-class.
        '''
        return type(self)((
            self.quality_string,
            abs(self.number),
            ))

    def __eq__(self, argument):
        r'''Is true when `argument` is a named interval-class with direction
        number, quality string and number equal to those of this named
        interval-class.

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
        except Exception:
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

    def _from_named_parts(self, direction, quality, diatonic_number):
        self._quality_string = constants._quality_abbreviation_to_quality_string[quality]
        diatonic_pc_number = diatonic_number
        while diatonic_pc_number > 7:
            diatonic_pc_number -= 7
        if diatonic_pc_number == 1 and diatonic_number >= 8:
            diatonic_pc_number = 8
        self._number = direction * diatonic_pc_number

    def _from_number(self, argument):
        direction, quality, diatonic_number = self._numbered_to_named(argument)
        self._from_named_parts(
            direction, quality, diatonic_number)

    def _from_interval_or_interval_class(self, argument):
        try:
            quality = constants._quality_string_to_quality_abbreviation[argument.quality_string]
            diatonic_number = abs(argument.number)
            direction = mathtools.sign(argument.number)
        except AttributeError:
            direction, quality, diatonic_number = self._numbered_to_named(argument)
        self._from_named_parts(
            direction, quality, diatonic_number)

    @property
    def _quality_abbreviation(self):
        return constants._quality_string_to_quality_abbreviation[
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
        import abjad
        named_interval = abjad.NamedInterval.from_pitch_carriers(
            pitch_carrier_1,
            pitch_carrier_2,
            )
        return class_(named_interval)
