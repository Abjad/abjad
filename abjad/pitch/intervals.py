import copy
import functools
import numbers
import typing

from .. import math
from ..storage import FormatSpecification, StorageFormatManager
from . import _lib
from .pitches import NamedPitch, NumberedPitch


# NOTE: mypy 0.770 errors on functools combined with abstract class
@functools.total_ordering
class Interval:
    """
    Abstract interval.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_interval_class", "_octaves")

    _is_abstract = True

    ### INITIALIZER ###

    def __init__(self, argument):
        if isinstance(argument, str):
            match = _lib._interval_name_abbreviation_regex.match(argument)
            if match is None:
                try:
                    argument = float(argument)
                    self._from_number(argument)
                    return
                except ValueError:
                    class_name = type(self).__name__
                    message = f"can not initialize {class_name} from {argument!r}."
                    raise ValueError(message)
                class_name = type(self).__name__
                message = f"can not initialize {class_name} from {argument!r}."
                raise ValueError(message)
            group_dict = match.groupdict()
            direction = group_dict["direction"]
            if direction == "-":
                direction = -1
            else:
                direction = 1
            quality = group_dict["quality"]
            diatonic_number = int(group_dict["number"])
            quality = self._validate_quality_and_diatonic_number(
                quality, diatonic_number
            )
            quartertone = group_dict["quartertone"]
            quality += quartertone
            self._from_named_parts(direction, quality, diatonic_number)
        elif isinstance(argument, tuple) and len(argument) == 2:
            quality, number = argument
            direction = math.sign(number)
            diatonic_number = abs(number)
            quality = self._validate_quality_and_diatonic_number(
                quality, diatonic_number
            )
            self._from_named_parts(direction, quality, diatonic_number)
        elif isinstance(argument, numbers.Number):
            self._from_number(argument)
        else:
            self._from_interval_or_interval_class(argument)

    ### SPECIAL METHODS ###

    def __abs__(self):
        """
        Gets absolute value of interval.

        Returns new interval.
        """
        raise NotImplementedError

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __float__(self):
        """
        Coerce to semitones as float.

        Returns float.
        """
        raise NotImplementedError

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __lt__(self, argument):
        """
        Is true when interval is less than ``argument``

        Returns true or false.
        """
        raise NotImplementedError

    def __neg__(self):
        """
        Negates interval.

        Returns interval.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self):
        """
        Gets string representation of interval.

        Returns string.
        """
        return str(self.number)

    ### PRIVATE METHODS ###

    def _from_interval_or_interval_class(self, argument):
        raise NotImplementedError

    def _from_named_parts(self, direction, quality, diatonic_number):
        raise NotImplementedError

    def _from_number(self, argument):
        raise NotImplementedError

    @classmethod
    def _named_to_numbered(cls, direction, quality, diatonic_number):
        octave_number = 0
        diatonic_pc_number = abs(diatonic_number)
        while diatonic_pc_number >= 8:
            diatonic_pc_number -= 7
            octave_number += 1

        quartertone = ""
        if quality.endswith(("+", "~")):
            quality, quartertone = quality[:-1], quality[-1]

        base_quality = quality
        if len(quality) > 1:
            base_quality = quality[0]

        semitones = _lib._diatonic_number_and_quality_to_semitones(
            diatonic_pc_number, base_quality
        )
        if base_quality == "d":
            semitones -= len(quality) - 1
        elif base_quality == "A":
            semitones += len(quality) - 1

        if quartertone == "+":
            semitones += 0.5
        elif quartertone == "~":
            semitones -= 0.5

        if abs(diatonic_number) == 1:
            semitones = abs(semitones)
        else:
            semitones += octave_number * 12
        semitones *= direction
        return math.integer_equivalent_number_to_integer(semitones)

    @classmethod
    def _numbered_to_named(cls, number):
        number = cls._to_nearest_quarter_tone(float(number))
        direction = math.sign(number)
        octaves, semitones = divmod(abs(number), 12)
        quartertone = ""
        if semitones % 1:
            semitones -= 0.5
            quartertone = "+"
        (
            quality,
            diatonic_number,
        ) = _lib._semitones_to_quality_and_diatonic_number[semitones]
        quality += quartertone
        diatonic_number += octaves * 7
        diatonic_number = cls._to_nearest_quarter_tone(diatonic_number)
        return direction, quality, diatonic_number

    @staticmethod
    def _to_nearest_quarter_tone(number):
        number = round(float(number) * 4) / 4
        div, mod = divmod(number, 1)
        if mod == 0.75:
            div += 1
        elif mod == 0.5:
            div += 0.5
        return math.integer_equivalent_number_to_integer(div)

    @classmethod
    def _validate_quality_and_diatonic_number(cls, quality, diatonic_number):
        if quality in _lib._quality_string_to_quality_abbreviation:
            quality = _lib._quality_string_to_quality_abbreviation[quality]
        if quality == "aug":
            quality = "A"
        if quality == "dim":
            quality = "d"
        octaves = 0
        diatonic_pc_number = diatonic_number
        while diatonic_pc_number > 7:
            diatonic_pc_number -= 7
            octaves += 1
        quality_to_semitones = _lib._diatonic_number_to_quality_dictionary[
            diatonic_pc_number
        ]
        if quality[0] not in quality_to_semitones:
            name = cls.__name__
            number = diatonic_number
            message = f"can not initialize {name} from {quality!r} and {number!r}."
            raise ValueError(message)
        return quality

    ### PUBLIC PROPERTIES ###

    @property
    def cents(self):
        """
        Gets cents of interval.

        Returns nonnegative number.
        """
        return 100 * self.semitones

    @property
    def direction_number(self):
        """
        Gets direction number of interval

        Returns integer.
        """
        raise NotImplementedError

    @property
    def interval_class(self):
        """
        Gets interval-class of interval.

        Returns interval-class.
        """
        raise NotImplementedError

    @property
    def number(self):
        """
        Gets number of interval.

        Returns integer.
        """
        raise NotImplementedError

    @property
    def octaves(self):
        """
        Gets octaves of interval.

        Returns nonnegative number.
        """
        raise NotImplementedError

    @property
    def semitones(self):
        """
        Gets semitones of interval.

        Returns integer or float.
        """
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def transpose(self, pitch_carrier):
        """
        Transposes ``pitch_carrier`` by interval.

        Returns new pitch carrier.
        """
        if hasattr(pitch_carrier, "transpose"):
            return pitch_carrier.transpose(self)
        elif hasattr(pitch_carrier, "written_pitch"):
            new_note = copy.copy(pitch_carrier)
            new_pitch = pitch_carrier.written_pitch.transpose(self)
            new_note.written_pitch = new_pitch
            return new_note
        elif hasattr(pitch_carrier, "written_pitches"):
            new_chord = copy.copy(pitch_carrier)
            pairs = zip(new_chord.note_heads, pitch_carrier.note_heads)
            for new_nh, old_nh in pairs:
                new_pitch = old_nh.written_pitch.transpose(self)
                new_nh.written_pitch = new_pitch
            return new_chord
        return pitch_carrier


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

    def __init__(self, name="P1"):
        super().__init__(name or "P1")

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
        return type(self)((self.quality, abs(self.number)))

    def __add__(self, argument):
        """
        Adds ``argument`` to named interval.

        ..  container:: example

            >>> abjad.NamedInterval('M9') + abjad.NamedInterval('M2')
            NamedInterval('+M10')

        Returns new named interval.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        dummy_pitch = NamedPitch(0)
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
        return type(self)((self.quality, self.number))

    def __eq__(self, argument):
        """
        Is true when named interval equal ``argument``

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
        Is true when ``argument`` is a named interval with a number greater
        than that of this named interval.

        ..  container:: example

            >>> abjad.NamedInterval('+M9') < abjad.NamedInterval('+M10')
            True

        ..  container:: example

            Also true when ``argument`` is a named interval with a
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

    def __mul__(self, argument) -> "NamedInterval":
        """
        Multiplies named interval by ``argument``

        ..  container:: example

            >>> 3 * abjad.NamedInterval('+M9')
            NamedInterval('+A25')

        """
        if not isinstance(argument, int):
            raise TypeError(f"must be integer: {argument!r}.")
        dummy_pitch = NamedPitch(0)
        for i in range(abs(argument)):
            dummy_pitch += self
        result = NamedInterval.from_pitch_carriers(NamedPitch(0), dummy_pitch)
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
        return type(self)((self.quality, -self.number))

    def __radd__(self, argument):
        """
        Adds named interval to ``argument``

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
        Multiplies ``argument`` by named interval.

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

    def __sub__(self, argument) -> "NamedInterval":
        """
        Subtracts ``argument`` from named interval.

        ..  container:: example

            >>> abjad.NamedInterval('+M9') - abjad.NamedInterval('+M2')
            NamedInterval('+P8')

            >>> abjad.NamedInterval('+M2') - abjad.NamedInterval('+M9')
            NamedInterval('-P8')

        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        dummy_pitch = NamedPitch(0)
        new_pitch = dummy_pitch + self - argument
        return NamedInterval.from_pitch_carriers(dummy_pitch, new_pitch)

    ### PRIVATE METHODS ###

    def _from_interval_or_interval_class(self, argument):
        try:
            quality = argument.quality
            diatonic_number = abs(argument.number)
            direction = math.sign(argument.number)
        except AttributeError:
            direction, quality, diatonic_number = self._numbered_to_named(argument)
        self._from_named_parts(direction, quality, diatonic_number)

    def _from_named_parts(self, direction, quality, diatonic_number):
        from .intervalclasses import NamedIntervalClass

        octaves = 0
        diatonic_pc_number = abs(diatonic_number)
        while diatonic_pc_number > 7:
            octaves += 1
            diatonic_pc_number -= 7
        if diatonic_pc_number == 1 and quality == "P" and diatonic_number >= 8:
            octaves -= 1
            diatonic_pc_number = 8
        self._octaves = octaves
        if direction:
            diatonic_pc_number *= direction
        self._interval_class = NamedIntervalClass((quality, diatonic_pc_number))

    def _from_number(self, argument):
        direction, quality, diatonic_number = self._numbered_to_named(argument)
        self._from_named_parts(direction, quality, diatonic_number)

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
        if self.quality == "P" and abs(self.number) == 1:
            return 0
        return math.sign(self.number)

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
        direction_symbol = _lib._direction_number_to_direction_symbol[
            self.direction_number
        ]
        return "{}{}{}".format(
            direction_symbol, self._interval_class.quality, abs(self.number)
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
        direction = math.sign(number)
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
            self.quality, diatonic_number
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
    def from_pitch_carriers(
        class_, pitch_carrier_1, pitch_carrier_2
    ) -> "NamedInterval":
        """
        Makes named interval calculated from ``pitch_carrier_1`` to
        ``pitch_carrier_2``

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

            >>> abjad.NamedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch("ds'"),
            ...     abjad.NamedPitch("ef''"),
            ...     )
            NamedInterval('+d9')

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

            >>> abjad.NamedInterval.from_pitch_carriers("c'", "d''")
            NamedInterval('+M9')

            >>> abjad.NamedInterval.from_pitch_carriers("c'", "df''")
            NamedInterval('+m9')

            >>> abjad.NamedInterval.from_pitch_carriers("c'", "dff''")
            NamedInterval('+d9')

            >>> abjad.NamedInterval.from_pitch_carriers("c'", "dfff''")
            NamedInterval('+dd9')

            >>> abjad.NamedInterval.from_pitch_carriers("c'", "dffff''")
            NamedInterval('+ddd9')

        """
        pitch_1 = NamedPitch(pitch_carrier_1)
        pitch_2 = NamedPitch(pitch_carrier_2)
        degree_1 = pitch_1._get_diatonic_pitch_number()
        degree_2 = pitch_2._get_diatonic_pitch_number()
        named_sign = math.sign(degree_1 - degree_2)
        named_i_number = abs(degree_1 - degree_2) + 1
        numbered_sign = math.sign(
            float(NumberedPitch(pitch_1)) - float(NumberedPitch(pitch_2))
        )
        numbered_i_number = abs(
            float(NumberedPitch(pitch_1)) - float(NumberedPitch(pitch_2))
        )
        (
            octaves,
            named_ic_number,
        ) = _lib._diatonic_number_to_octaves_and_diatonic_remainder(named_i_number)
        numbered_ic_number = numbered_i_number - 12 * octaves

        # multiply-diminished intervals can have opposite signs
        if named_sign and (named_sign == -numbered_sign):
            numbered_ic_number *= -1

        quartertone = ""
        if numbered_ic_number % 1:
            quartertone = "+"
            numbered_ic_number -= 0.5

        quality_to_semitones = _lib._diatonic_number_to_quality_dictionary[
            named_ic_number
        ]

        semitones_to_quality: typing.Dict = {
            value: key for key, value in quality_to_semitones.items()
        }

        quality = ""

        while numbered_ic_number > max(semitones_to_quality):
            numbered_ic_number -= 1
            quality += "A"

        while numbered_ic_number < min(semitones_to_quality):
            numbered_ic_number += 1
            quality += "d"

        quality += semitones_to_quality[numbered_ic_number]
        quality += quartertone
        direction = 1
        if pitch_2 < pitch_1:
            direction = -1

        return class_((quality, named_i_number * direction))

    def transpose(self, pitch_carrier):
        """
        Transposes ``pitch_carrier`` by named interval.

        ..  container:: example

            Transposes chord:

            >>> chord = abjad.Chord("<c' e' g'>4")

            >>> interval = abjad.NamedInterval('+m2')
            >>> interval.transpose(chord)
            Chord("<df' f' af'>4")

        Returns new (copied) object of ``pitch_carrier`` type.
        """
        return super().transpose(pitch_carrier)


class NumberedInterval(Interval):
    """
    Numbered interval.

    ..  container:: example

        Initializes from number of semitones:

        >>> abjad.NumberedInterval(-14)
        NumberedInterval(-14)

    ..  container:: example

        Initializes from other numbered interval

        >>> abjad.NumberedInterval(abjad.NumberedInterval(-14))
        NumberedInterval(-14)

    ..  container:: example

        Initializes from named interval:

        >>> abjad.NumberedInterval(abjad.NamedInterval('-P4'))
        NumberedInterval(-5)

    ..  container:: example

        Initializes from interval string:

        >>> abjad.NumberedInterval('-P4')
        NumberedInterval(-5)

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, number=0):
        super().__init__(number or 0)

    ### SPECIAL METHODS ###

    def __abs__(self):
        """
        Absolute value of numbered interval.

        ..  container:: example

            >>> abs(abjad.NumberedInterval(-14))
            NumberedInterval(14)

        Returns new numbered interval.
        """
        return type(self)(abs(self.number))

    def __add__(self, argument):
        """
        Adds ``argument`` to numbered interval.

        ..  container:: example

            >>> abjad.NumberedInterval(3) + abjad.NumberedInterval(14)
            NumberedInterval(17)

            >>> abjad.NumberedInterval(3) + abjad.NumberedInterval(-14)
            NumberedInterval(-11)

        Returns new numbered interval.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return type(self)(float(self) + float(argument))

    def __copy__(self):
        """
        Copies numbered interval.

        >>> import copy

        ..  container:: example

            >>> copy.copy(abjad.NumberedInterval(-14))
            NumberedInterval(-14)

        Returns new numbered interval.
        """
        return type(self)(self.number)

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a numbered interval with number equal to that of
        this numbered interval.

        ..  container:: example

            >>> interval_1 = abjad.NumberedInterval(12)
            >>> interval_2 = abjad.NumberedInterval(12)
            >>> interval_3 = abjad.NumberedInterval(13)

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

        Returns true or false.
        """
        return super().__eq__(argument)

    def __float__(self):
        """
        Coerce to float.

        Returns float.
        """
        return float(self.number)

    def __hash__(self):
        """
        Hashes numbered interval.

        Returns integer.
        """
        return super().__hash__()

    def __lt__(self, argument):
        """
        Is true when ``argument`` is a numbered interval with same direction
        number as this numbered interval and with number greater than that of
        this numbered interval.

        ..  container:: example

            >>> interval_1 = abjad.NumberedInterval(12)
            >>> interval_2 = abjad.NumberedInterval(12)
            >>> interval_3 = abjad.NumberedInterval(13)

            >>> interval_1 < interval_1
            False

            >>> interval_1 < interval_2
            False

            >>> interval_1 < interval_3
            True

            >>> interval_2 < interval_1
            False

            >>> interval_2 < interval_2
            False

            >>> interval_2 < interval_3
            True

            >>> interval_3 < interval_1
            False

            >>> interval_3 < interval_2
            False

            >>> interval_3 < interval_3
            False

        Returns true or false.
        """
        if not isinstance(argument, type(self)):
            raise TypeError(f"must be numbered interval: {argument!r}.")
        if not self.direction_number == argument.direction_number:
            raise ValueError("can only compare intervals of same direction.")
        return abs(self.number) < abs(argument.number)

    def __neg__(self):
        """
        Negates numbered interval.

        ..  container:: example

            >>> -abjad.NumberedInterval(-14)
            NumberedInterval(14)

        Returns new numbered interval.
        """
        return type(self)(-self.number)

    def __radd__(self, argument):
        """
        Adds numbered interval to ``argument``

        ..  container:: example

            >>> interval = abjad.NumberedInterval(14)
            >>> abjad.NumberedInterval(3).__radd__(interval)
            NumberedInterval(17)

            >>> interval = abjad.NumberedInterval(-14)
            >>> abjad.NumberedInterval(3).__radd__(interval)
            NumberedInterval(-11)

        Returns new numbered interval.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return type(self)(float(self) + float(argument))

    def __str__(self):
        """
        String representation of numbered interval.

        Returns string.
        """
        direction_symbol = _lib._direction_number_to_direction_symbol[
            math.sign(self.number)
        ]
        return f"{direction_symbol}{abs(self.number)}"

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from numbered interval.

        Returns new numbered interval.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return type(self)(float(self) - float(argument))

    ### PRIVATE METHODS ###

    def _from_interval_or_interval_class(self, argument):
        self._from_number(float(argument))

    def _from_named_parts(self, direction, quality, diatonic_number):
        self._from_number(self._named_to_numbered(direction, quality, diatonic_number))

    def _from_number(self, argument):
        from .intervalclasses import NumberedIntervalClass

        number = self._to_nearest_quarter_tone(argument)
        direction = math.sign(number)
        octaves = 0
        pc_number = abs(number)
        while pc_number > 12:
            pc_number -= 12
            octaves += 1
        self._octaves = octaves
        self._interval_class = NumberedIntervalClass(pc_number * direction)

    def _get_format_specification(self):
        values = [self.number]
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
        Gets direction number of numbered interval.

        ..  container:: example

            >>> abjad.NumberedInterval(-14).direction_number
            -1

            >>> abjad.NumberedInterval(0).direction_number
            0

            >>> abjad.NumberedInterval(6).direction_number
            1

        Returns integer.
        """ ""
        return math.sign(self.number)

    @property
    def interval_class(self):
        """
        Gets interval class of numbered interval.

        Returns numbered interval-class.
        """
        return self._interval_class

    @property
    def number(self):
        """
        Gets number of numbered interval.

        ..  container:: example

            >>> abjad.NumberedInterval(-14).number
            -14

            >>> abjad.NumberedInterval(-2).number
            -2

            >>> abjad.NumberedInterval(0).number
            0

        Returns number.
        """
        number = self._interval_class._number
        direction = math.sign(number)
        number = abs(number) + (12 * self.octaves)
        return number * direction

    @property
    def octaves(self):
        """
        Gets octaves of interval.

        Returns nonnegative number.
        """
        return self._octaves

    @property
    def semitones(self):
        """
        Gets semitones corresponding to numbered interval.

        ..  container:: example

            >>> abjad.NumberedInterval(-14).semitones
            -14

        Returns nonnegative number.
        """
        return self.number

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(
        class_, pitch_carrier_1, pitch_carrier_2
    ) -> "NumberedInterval":
        """Makes numbered interval from ``pitch_carrier_1`` and
        ``pitch_carrier_2``

        ..  container:: example

            >>> abjad.NumberedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch(-2),
            ...     abjad.NamedPitch(12),
            ...     )
            NumberedInterval(14)

            >>> abjad.NumberedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(12),
            ...     )
            NumberedInterval(0)

            >>> abjad.NumberedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch(9),
            ...     abjad.NamedPitch(12),
            ...     )
            NumberedInterval(3)

            >>> abjad.NumberedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(9),
            ...     )
            NumberedInterval(-3)

            >>> abjad.NumberedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(-2),
            ...     )
            NumberedInterval(-14)

        """
        pitch_1 = NamedPitch(pitch_carrier_1)
        pitch_2 = NamedPitch(pitch_carrier_2)
        number = NumberedPitch(pitch_2).number - NumberedPitch(pitch_1).number
        number = math.integer_equivalent_number_to_integer(number)
        return class_(number)

    def transpose(self, pitch_carrier):
        """
        Transposes ``pitch_carrier``

        ..  container:: example

            Transposes chord:

            >>> chord = abjad.Chord("<c' e' g'>4")

            >>> interval = abjad.NumberedInterval(1)
            >>> interval.transpose(chord)
            Chord("<df' f' af'>4")

        Returns newly constructed object of ``pitch_carrier`` type.
        """
        return super().transpose(pitch_carrier)
