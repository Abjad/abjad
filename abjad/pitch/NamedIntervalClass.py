from abjad import mathtools
from . import constants
from abjad.system.FormatSpecification import FormatSpecification
from .IntervalClass import IntervalClass


class NamedIntervalClass(IntervalClass):
    """
    Named interval-class.

    ..  container:: example

        Initializes from name:

        >>> abjad.NamedIntervalClass('-M9')
        NamedIntervalClass('-M2')

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        '_quality',
        )

    ### INITIALIZER ###

    def __init__(self, name='P1'):
        super().__init__(name or 'P1')

    ### SPECIAL METHODS ###

    def __abs__(self):
        """
        Gets absolute value of named interval-class.

        ..  container:: example

            >>> abs(abjad.NamedIntervalClass('-M9'))
            NamedIntervalClass('+M2')

        Returns new named interval-class.
        """
        return type(self)((
            self.quality,
            abs(self.number),
            ))

    def __add__(self, argument):
        """
        Adds `argument` to named interval-class.

        Returns new named interval-class.
        """
        import abjad
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        dummy_pitch = abjad.NamedPitch(0)
        new_pitch = dummy_pitch + self + argument
        interval = abjad.NamedInterval.from_pitch_carriers(
            dummy_pitch,
            new_pitch,
            )
        return type(self)(interval)

    def __eq__(self, argument):
        """
        Is true when `argument` is a named interval-class with direction
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
        """
        return super().__eq__(argument)

    def __float__(self):
        """
        Coerce to float.

        Returns float.
        """
        return float(self._named_to_numbered(
            self.direction_number,
            self._quality,
            abs(self._number),
            ))

    def __hash__(self):
        """
        Hashes named interval-class.

        Returns integer.
        """
        return super().__hash__()

    def __lt__(self, argument):
        """
        Is true when `argument` is a named interval class with a number
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
        """
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

    def __radd__(self, argument):
        """
        Adds interval-class to `argument`.

        Returns new named interval-class.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return argument.__add__(self)

    def __str__(self):
        """
        Gets string representation of named interval-class.

        ..  container:: example

            >>> str(abjad.NamedIntervalClass('-M9'))
            '-M2'

        Returns string.
        """
        return self.name

    def __sub__(self, argument):
        """
        Subtracts `argument` from named interval-class.

        Returns new named interval-class.
        """
        import abjad
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        dummy_pitch = abjad.NamedPitch(0)
        new_pitch = dummy_pitch + self - argument
        interval = abjad.NamedInterval.from_pitch_carriers(
            dummy_pitch,
            new_pitch,
            )
        return type(self)(interval)

    ### PRIVATE PROPERTIES ###

    def _from_named_parts(self, direction, quality, diatonic_number):
        self._quality = quality
        diatonic_pc_number = diatonic_number
        while diatonic_pc_number > 7:
            diatonic_pc_number -= 7
        if diatonic_pc_number == 1 and diatonic_number >= 8:
            if quality == 'P':
                diatonic_pc_number = 8
            elif quality.startswith('d') or quality == 'P~':
                direction *= -1
        if not (diatonic_number == 1 and quality == 'P'):
            diatonic_pc_number *= direction
        self._number = diatonic_pc_number

    def _from_number(self, argument):
        direction, quality, diatonic_number = self._numbered_to_named(argument)
        self._from_named_parts(direction, quality, diatonic_number)

    def _from_interval_or_interval_class(self, argument):
        try:
            quality = argument.quality
            diatonic_number = abs(argument.number)
            direction = mathtools.sign(argument.number)
        except AttributeError:
            direction, quality, diatonic_number = self._numbered_to_named(argument)
        self._from_named_parts(direction, quality, diatonic_number)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.name]
        return FormatSpecification(
            client=self,
            coerce_for_equality=True,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def direction_number(self):
        """
        Gets direction number of named interval-class.

        ..  container:: example

            >>> abjad.NamedIntervalClass('P1').direction_number
            0

            >>> abjad.NamedIntervalClass('+M2').direction_number
            1

            >>> abjad.NamedIntervalClass('-M2').direction_number
            -1

        Returns -1, 0 or 1.
        """
        if self.quality == 'P' and abs(self.number) == 1:
            return 0
        return mathtools.sign(self.number)

    @property
    def name(self):
        """
        Gets name of named interval-class.

        ..  container:: example

            >>> abjad.NamedIntervalClass('-M9').name
            '-M2'

        Returns string.
        """
        return '{}{}{}'.format(
            constants._direction_number_to_direction_symbol[
                self.direction_number],
            self._quality,
            abs(self.number),
            )

    @property
    def quality(self):
        """
        Gets quality of named interval-class.

        Returns string.
        """
        return self._quality

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(class_, pitch_carrier_1, pitch_carrier_2):
        """
        Makes named interval-class from `pitch_carrier_1` and
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
        """
        import abjad
        named_interval = abjad.NamedInterval.from_pitch_carriers(
            pitch_carrier_1,
            pitch_carrier_2,
            )
        return class_(named_interval)
