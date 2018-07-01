from abjad import mathtools
from abjad.system.FormatSpecification import FormatSpecification
from .IntervalClass import IntervalClass


class NumberedIntervalClass(IntervalClass):
    """
    Numbered interval-class.

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

        >>> abjad.NumberedIntervalClass('P8')
        NumberedIntervalClass(12)

        >>> abjad.NumberedIntervalClass('-P8')
        NumberedIntervalClass(-12)

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    ### INITIALIZER ###

    def __init__(self, number=0):
        super().__init__(number or 0)

    ### SPECIAL METHODS ###

    def __abs__(self):
        """
        Gets absolute value of numbered interval-class.

        Returns new numbered interval-class.
        """
        return type(self)(abs(self.number))

    def __add__(self, argument):
        """
        Adds `argument` to numbered interval-class.

        Returns new numbered interval-class.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return type(self)(float(self) + float(argument))

    def __radd__(self, argument):
        """
        Adds `argument` to numbered interval-class.

        Returns new numbered interval-class.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return type(self)(float(self) + float(argument))

    def __eq__(self, argument):
        """
        Is true when `argument` is a numbered interval-class with number
        equal to that of this numbered interval-class.

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
        """
        return super().__eq__(argument)

    def __float__(self):
        """
        Coerce to semitones as float.

        Returns float.
        """
        return float(self._number)

    def __hash__(self):
        """
        Hashes numbered interval-class.

        Returns integer.
        """
        return super().__hash__()

    def __lt__(self, argument):
        """
        Is true when numbered interval-class is less than `argument`.

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
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return False
        return self.number < argument.number

    def __str__(self):
        """
        Gets string representation of numbered interval-class.

        ..  container:: example

            >>> str(abjad.NumberedIntervalClass(-13))
            '-1'

            >>> str(abjad.NumberedIntervalClass(0))
            '0'

            >>> str(abjad.NumberedIntervalClass(13))
            '+1'

        """
        string = super().__str__()
        if 0 < self.number:
            string = '+' + string
        return string

    def __sub__(self, argument):
        """
        Subtracts `argument` from numbered interval-class.

        Returns new numbered interval-class.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return type(self)(float(self) - float(argument))

    ### PRIVATE METHODS ###

    def _from_named_parts(self, direction, quality, diatonic_number):
        self._number = self._named_to_numbered(
            direction,
            quality,
            diatonic_number,
            )

    def _from_number(self, argument):
        direction = mathtools.sign(argument)
        number = self._to_nearest_quarter_tone(abs(argument))
        pc_number = number % 12
        if pc_number == 0 and number:
            pc_number = 12
        self._number = pc_number * direction

    def _from_interval_or_interval_class(self, argument):
        self._from_number(float(argument))

    def _get_format_specification(self):
        return FormatSpecification(
            client=self,
            coerce_for_equality=True,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=[self.number],
            )

    ### PUBLIC PROPERTIES ###

    @property
    def direction_number(self):
        """
        Gets direction number of numbered interval-class.

        Returns -1, 0 or 1.
        """
        if self.number < 1:
            return -1
        elif self.number == 1:
            return 0
        else:
            return 1

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(class_, pitch_carrier_1, pitch_carrier_2):
        """Makes numbered interval-class from `pitch_carrier_1` and
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
            ...     abjad.NamedPitch(24),
            ...     abjad.NamedPitch(0),
            ...     )
            NumberedIntervalClass(-12)

            >>> abjad.NumberedIntervalClass.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(-2),
            ...     )
            NumberedIntervalClass(-2)

        Returns numbered interval-class.
        """
        import abjad
        interval = abjad.NumberedInterval.from_pitch_carriers(
            pitch_carrier_1,
            pitch_carrier_2,
            )
        return class_(interval)
