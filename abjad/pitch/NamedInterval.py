from abjad import mathtools
from abjad.system.FormatSpecification import FormatSpecification
from . import constants
from .Interval import Interval


class NamedInterval(Interval):
    """
    Named interval.

    ..  container:: example

        Initializes ascending major ninth from string:

        >>> abjad.NamedInterval('+M9')
        NamedInterval('+M9')

    ..  container:: example

        Initializes descending major third from number of semitones:

        >>> abjad.NamedInterval(-4)
        NamedInterval('-M3')

    ..  container:: example

        Initializes from other named interval:

        >>> abjad.NamedInterval(abjad.NamedInterval(-4))
        NamedInterval('-M3')

    ..  container:: example

        Initializes from numbered interval:

        >>> abjad.NamedInterval(abjad.NumberedInterval(3))
        NamedInterval('+m3')

    ..  container:: example

        Initializes from pair of quality and diatonic number:

        >>> abjad.NamedInterval(('M', 3))
        NamedInterval('+M3')

    """

    ### CLASS VARIABLES ##

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, name='P1'):
        super().__init__(name or 'P1')

    ### SPECIAL METHODS ###

    def __abs__(self):
        """
        Gets absolute value of named interval.

        ..  container:: example

            >>> abs(abjad.NamedInterval('+M9'))
            NamedInterval('+M9')

            >>> abs(abjad.NamedInterval('-M9'))
            NamedInterval('+M9')

        Returns named interval.
        """
        return type(self)((
            self.quality,
            abs(self.number),
            ))

    def __add__(self, argument):
        """
        Adds `argument` to named interval.

        ..  container:: example

            >>> abjad.NamedInterval('M9') + abjad.NamedInterval('M2')
            NamedInterval('+M10')

        Returns new named interval.
        """
        import abjad
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        dummy_pitch = abjad.NamedPitch(0)
        new_pitch = dummy_pitch + self + argument
        return NamedInterval.from_pitch_carriers(dummy_pitch, new_pitch)

    def __copy__(self, *arguments):
        """
        Copies named interval.

        >>> import copy

        ..  container:: example

            >>> copy.copy(abjad.NamedInterval('+M9'))
            NamedInterval('+M9')

        Returns new named interval.
        """
        return type(self)((
            self.quality,
            self.number,
            ))

    def __eq__(self, argument):
        """
        Is true when named interval equal `argument`.

        ..  container:: example

            >>> interval_1 = abjad.NamedInterval('m2')
            >>> interval_2 = abjad.NamedInterval('m2')
            >>> interval_3 = abjad.NamedInterval('m9')

            >>> interval_1 == interval_1
            True
            >>> interval_1 == interval_2
            True
            >>> interval_1 == interval_3
            False

            >>> interval_2 == interval_1
            True
            >>> interval_2 == interval_2
            True
            >>> interval_2 == interval_3
            False

            >>> interval_3 == interval_1
            False
            >>> interval_3 == interval_2
            False
            >>> interval_3 == interval_3
            True

        """
        return super().__eq__(argument)

    def __float__(self):
        """
        Coerce to semitones as float.

        Returns float.
        """
        return float(self.semitones)

    def __hash__(self):
        """
        Hashes named interval.

        Returns number.
        """
        return super().__hash__()

    def __lt__(self, argument):
        """
        Is true when `argument` is a named interval with a number greater
        than that of this named interval.

        ..  container:: example

            >>> abjad.NamedInterval('+M9') < abjad.NamedInterval('+M10')
            True

        ..  container:: example

            Also true when `argument` is a named interval with a
            number equal to this named interval and with semitones greater than
            this named interval:

            >>> abjad.NamedInterval('+m9') < abjad.NamedInterval('+M9')
            True

        ..  container:: example

            Otherwise false:

            >>> abjad.NamedInterval('+M9') < abjad.NamedInterval('+M2')
            False

        Returns true or false.
        """
        if isinstance(argument, type(self)):
            if self.number == argument.number:
                return self.semitones < argument.semitones
            return self.number < argument.number
        return False

    def __mul__(self, argument):
        """
        Multiplies named interval by `argument`.

        ..  container:: example

            >>> 3 * abjad.NamedInterval('+M9')
            NamedInterval('+A25')

        Returns new named interval.
        """
        import abjad
        if not isinstance(argument, int):
            message = 'must be integer: {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        dummy_pitch = abjad.NamedPitch(0)
        for i in range(abs(argument)):
            dummy_pitch += self
        result = NamedInterval.from_pitch_carriers(
            abjad.NamedPitch(0),
            dummy_pitch,
            )
        if argument < 0:
            return -result
        return result

    def __neg__(self):
        """
        Negates named interval.

        ..  container:: example

            >>> -abjad.NamedInterval('+M9')
            NamedInterval('-M9')

        ..  container:: example

            >>> -abjad.NamedInterval('-M9')
            NamedInterval('+M9')

        Returns new named interval.
        """
        return type(self)((
            self.quality,
            -self.number,
            ))

    def __radd__(self, argument):
        """
        Adds named interval to `argument`.

        ..  container:: example

            >>> abjad.NamedInterval('M9') + abjad.NamedInterval('M2')
            NamedInterval('+M10')

        Returns new named interval.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return argument.__add__(self)

    def __rmul__(self, argument):
        """
        Multiplies `argument` by named interval.

        ..  container:: example

            >>> abjad.NamedInterval('+M9') * 3
            NamedInterval('+A25')

        Returns new named interval.
        """
        return self * argument

    def __str__(self):
        """
        Gets string representation of named interval.

        ..  container:: example

            >>> str(abjad.NamedInterval('+M9'))
            '+M9'

        Returns string.
        """
        return self.name

    def __sub__(self, argument):
        """
        Subtracts `argument` from named interval.

        ..  container:: example

            >>> abjad.NamedInterval('+M9') - abjad.NamedInterval('+M2')
            NamedInterval('+P8')

            >>> abjad.NamedInterval('+M2') - abjad.NamedInterval('+M9')
            NamedInterval('-P8')

        Returns new named interval.
        """
        import abjad
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        dummy_pitch = abjad.NamedPitch(0)
        new_pitch = dummy_pitch + self - argument
        return NamedInterval.from_pitch_carriers(dummy_pitch, new_pitch)

    ### PRIVATE PROPERTIES ###

    def _from_named_parts(self, direction, quality, diatonic_number):
        import abjad
        octaves = 0
        diatonic_pc_number = abs(diatonic_number)
        while diatonic_pc_number > 7:
            octaves += 1
            diatonic_pc_number -= 7
        if diatonic_pc_number == 1 and quality == 'P' and diatonic_number >= 8:
            octaves -= 1
            diatonic_pc_number = 8
        self._octaves = octaves
        if direction:
            diatonic_pc_number *= direction
        self._interval_class = abjad.NamedIntervalClass((
            quality,
            diatonic_pc_number,
            ))

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
        Gets direction number of named interval.

        ..  container:: example

            >>> abjad.NamedInterval('+M9').direction_number
            1

            >>> abjad.NamedInterval('+dim2').direction_number
            1

            >>> abjad.NamedInterval('+A1').direction_number
            1

            >>> abjad.NamedInterval('P1').direction_number
            0

            >>> abjad.NamedInterval('-m3').direction_number
            -1

        Returns ``-1``, ``0`` or ``1``.
        """
        if self.quality == 'P' and abs(self.number) == 1:
            return 0
        return mathtools.sign(self.number)

    @property
    def interval_class(self):
        """
        Gets interval class of named interval.

        ..  container:: example

            >>> abjad.NamedInterval('+M9').interval_class
            NamedIntervalClass('+M2')

            >>> abjad.NamedInterval('-M9').interval_class
            NamedIntervalClass('-M2')

            >>> abjad.NamedInterval('P1').interval_class
            NamedIntervalClass('P1')

            >>> abjad.NamedInterval('+P8').interval_class
            NamedIntervalClass('+P8')

        Returns named interval-class.
        """
        return self._interval_class

    @property
    def name(self):
        """
        Gets name of named interval.

        ..  container:: example

            >>> abjad.NamedInterval('+M9').name
            '+M9'

        Returns string.
        """
        direction_symbol = constants._direction_number_to_direction_symbol[
            self.direction_number]
        return '{}{}{}'.format(
            direction_symbol,
            self._interval_class.quality,
            abs(self.number),
            )

    @property
    def number(self):
        """
        Gets number of named interval.

        ..  container:: example

            >>> abjad.NamedInterval('+M9').number
            9

        Returns nonnegative number.
        """
        number = self._interval_class._number
        direction = mathtools.sign(number)
        number = abs(number) + (7 * self.octaves)
        return number * direction

    @property
    def octaves(self):
        """
        Gets octaves of interval.

        Returns nonnegative number.
        """
        return self._octaves

    @property
    def quality(self):
        """
        Gets quality of named interval.

        Returns string.
        """
        return self._interval_class.quality

    @property
    def semitones(self):
        """
        Gets semitones of named interval.

        ..  container:: example

            >>> abjad.NamedInterval('+M9').semitones
            14

            >>> abjad.NamedInterval('-M9').semitones
            -14

            >>> abjad.NamedInterval('P1').semitones
            0

            >>> abjad.NamedInterval('+P8').semitones
            12

            >>> abjad.NamedInterval('-P8').semitones
            -12

        Returns number.
        """
        direction = self.direction_number
        diatonic_number = abs(self._interval_class._number)
        quality = self._validate_quality_and_diatonic_number(
            self.quality, diatonic_number,
        )
        diatonic_number += 7 * self._octaves
        return self._named_to_numbered(direction, quality, diatonic_number)

    @property
    def staff_spaces(self):
        """
        Gets staff spaces of named interval.

        ..  container:: example

            >>> abjad.NamedInterval('+M9').staff_spaces
            8

            >>> abjad.NamedInterval('-M9').staff_spaces
            -8

            >>> abjad.NamedInterval('P1').staff_spaces
            0

            >>> abjad.NamedInterval('+P8').staff_spaces
            7

            >>> abjad.NamedInterval('-P8').staff_spaces
            -7

        Returns nonnegative integer.
        """
        if self.direction_number == -1:
            return self.number + 1
        elif not self.direction_number:
            return 0
        elif self.direction_number == 1:
            return self.number - 1

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(class_, pitch_carrier_1, pitch_carrier_2):
        """
        Makes named interval calculated from `pitch_carrier_1` to
        `pitch_carrier_2`.

        ..  container:: example

            >>> abjad.NamedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch(-2),
            ...     abjad.NamedPitch(12),
            ...     )
            NamedInterval('+M9')

            >>> abjad.NamedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch("css'"),
            ...     abjad.NamedPitch("cff'"),
            ...     )
            NamedInterval('-AAAA1')

            >>> abjad.NamedInterval.from_pitch_carriers("c'", "cs'''")
            NamedInterval('+A15')

            >>> abjad.NamedInterval.from_pitch_carriers('c', 'cqs')
            NamedInterval('+P+1')

            >>> abjad.NamedInterval.from_pitch_carriers("cf'", 'bs')
            NamedInterval('-dd2')

            >>> abjad.NamedInterval.from_pitch_carriers("cff'", 'aqs')
            NamedInterval('-ddd+3')

            >>> abjad.NamedInterval.from_pitch_carriers("cff'", 'atqs')
            NamedInterval('-dddd+3')

        Returns named interval.
        """
        import abjad

        pitch_1 = abjad.NamedPitch(pitch_carrier_1)
        pitch_2 = abjad.NamedPitch(pitch_carrier_2)
        degree_1 = pitch_1._get_diatonic_pitch_number()
        degree_2 = pitch_2._get_diatonic_pitch_number()
        named_sign = mathtools.sign(degree_1 - degree_2)
        named_i_number = abs(degree_1 - degree_2) + 1
        numbered_sign = mathtools.sign(
            float(abjad.NumberedPitch(pitch_1)) -
            float(abjad.NumberedPitch(pitch_2))
            )
        numbered_i_number = abs(
            float(abjad.NumberedPitch(pitch_1)) -
            float(abjad.NumberedPitch(pitch_2))
            )
        named_ic_number = named_i_number
        numbered_ic_number = numbered_i_number

        while named_ic_number > 8 and numbered_ic_number > 12:
            named_ic_number -= 7
            numbered_ic_number -= 12

        # Multiply-diminished intervals can have opposite signs
        if named_sign and (named_sign == -numbered_sign):
            numbered_ic_number *= -1

        quartertone = ''
        if numbered_ic_number % 1:
            quartertone = '+'
            numbered_ic_number -= 0.5

        mapping = {
            value: key
            for key, value in
            constants._diatonic_number_and_quality_to_semitones[
                named_ic_number].items()
            }

        quality = ''

        while numbered_ic_number > max(mapping):
            numbered_ic_number -= 1
            quality += 'A'

        while numbered_ic_number < min(mapping):
            numbered_ic_number += 1
            quality += 'd'

        quality += mapping[numbered_ic_number]
        quality += quartertone
        direction = 1
        if pitch_2 < pitch_1:
            direction = -1

        return class_((quality, named_i_number * direction))

    def transpose(self, pitch_carrier):
        """
        Transposes `pitch_carrier` by named interval.

        ..  container:: example

            Transposes chord:

            >>> chord = abjad.Chord("<c' e' g'>4")

            >>> interval = abjad.NamedInterval('+m2')
            >>> interval.transpose(chord)
            Chord("<df' f' af'>4")

        Returns new (copied) object of `pitch_carrier` type.
        """
        return super().transpose(pitch_carrier)
