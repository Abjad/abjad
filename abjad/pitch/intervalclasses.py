import copy
import functools
import numbers

from .. import math
from ..storage import FormatSpecification, StorageFormatManager
from . import _lib
from .intervals import Interval, NamedInterval, NumberedInterval
from .pitches import NamedPitch


@functools.total_ordering
class IntervalClass:
    """
    Abstract interval-class.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

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
                    message = (
                        f"can not initialize {type(self).__name__} from {argument!r}."
                    )
                    raise ValueError(message)
                message = f"can not initialize {type(self).__name__} from {argument!r}."
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
        elif isinstance(argument, (Interval, IntervalClass)):
            self._from_interval_or_interval_class(argument)
        else:
            message = f"can not initialize {type(self).__name__} from {argument!r}."
            raise ValueError(message)

    ### SPECIAL METHODS ###

    def __abs__(self):
        """
        Gets absolute value of interval-class.

        Returns new interval-class.
        """
        return type(self)(abs(self._number))

    def __add__(self, argument):
        """
        Adds ``argument`` to interval-class.

        Returns new interval-class.
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
        Is true when interval-class is less than ``argument``

        Returns true or false.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self):
        """
        Gets string representation of interval-class.

        Returns string.
        """
        return str(self.number)

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from interval-class.

        Returns new interval-class.
        """
        raise NotImplementedError

    ### PRIVATE METHODS ###

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
        if base_quality == "P" and octave_number and diatonic_pc_number == 1:
            return 12 * direction
        if len(quality) > 1:
            base_quality = quality[0]

        semitones = _lib._diatonic_number_and_quality_to_semitones(
            diatonic_pc_number,
            base_quality,
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
        while abs(semitones) > 12:
            semitones = (abs(semitones) - 12) * math.sign(semitones)
        semitones *= direction
        return math.integer_equivalent_number_to_integer(semitones)

    @classmethod
    def _numbered_to_named(cls, number):
        number = cls._to_nearest_quarter_tone(float(number))
        direction = math.sign(number)
        octaves, semitones = divmod(abs(number), 12)
        if semitones == 0 and octaves:
            semitones = 12
        quartertone = ""
        if semitones % 1:
            semitones -= 0.5
            quartertone = "+"
        (
            quality,
            diatonic_pc_number,
        ) = _lib._semitones_to_quality_and_diatonic_number[semitones]
        quality += quartertone
        diatonic_pc_number = cls._to_nearest_quarter_tone(diatonic_pc_number)
        return direction, quality, diatonic_pc_number

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
    def number(self):
        """
        Gets number of interval-class.

        Returns number.
        """
        return self._number

    ### PUBLIC METHODS ###

    def transpose(self, pitch_carrier):
        """
        Transposes ``pitch_carrier`` by interval-class.

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


class NamedIntervalClass(IntervalClass):
    """
    Named interval-class.

    ..  container:: example

        Initializes from name:

        >>> abjad.NamedIntervalClass('-M9')
        NamedIntervalClass('-M2')

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_number", "_quality")

    ### INITIALIZER ###

    def __init__(self, name="P1"):
        super().__init__(name or "P1")

    ### SPECIAL METHODS ###

    def __abs__(self):
        """
        Gets absolute value of named interval-class.

        ..  container:: example

            >>> abs(abjad.NamedIntervalClass('-M9'))
            NamedIntervalClass('+M2')

        Returns new named interval-class.
        """
        return type(self)((self.quality, abs(self.number)))

    def __add__(self, argument):
        """
        Adds ``argument`` to named interval-class.

        Returns new named interval-class.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        dummy_pitch = NamedPitch(0)
        new_pitch = dummy_pitch + self + argument
        interval = NamedInterval.from_pitch_carriers(dummy_pitch, new_pitch)
        return type(self)(interval)

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a named interval-class with direction
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
        return float(
            self._named_to_numbered(
                self.direction_number, self._quality, abs(self._number)
            )
        )

    def __hash__(self):
        """
        Hashes named interval-class.

        Returns integer.
        """
        return super().__hash__()

    def __lt__(self, argument):
        """
        Is true when ``argument`` is a named interval class with a number
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
        try:
            argument = type(self)(argument)
        except Exception:
            return False
        if self.number == argument.number:
            self_semitones = NamedInterval(self).semitones
            argument_semitones = NamedInterval(argument).semitones
            return self_semitones < argument_semitones
        return self.number < argument.number

    def __radd__(self, argument):
        """
        Adds interval-class to ``argument``

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
        Subtracts ``argument`` from named interval-class.

        Returns new named interval-class.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        dummy_pitch = NamedPitch(0)
        new_pitch = dummy_pitch + self - argument
        interval = NamedInterval.from_pitch_carriers(dummy_pitch, new_pitch)
        return type(self)(interval)

    ### PRIVATE PROPERTIES ###

    def _from_interval_or_interval_class(self, argument):
        try:
            quality = argument.quality
            diatonic_number = abs(argument.number)
            direction = math.sign(argument.number)
        except AttributeError:
            direction, quality, diatonic_number = self._numbered_to_named(argument)
        self._from_named_parts(direction, quality, diatonic_number)

    def _from_named_parts(self, direction, quality, diatonic_number):
        self._quality = quality
        diatonic_pc_number = diatonic_number
        while diatonic_pc_number > 7:
            diatonic_pc_number -= 7
        if diatonic_pc_number == 1 and diatonic_number >= 8:
            if quality == "P":
                diatonic_pc_number = 8
            elif quality.startswith("d") or quality == "P~":
                direction *= -1
        if not (diatonic_number == 1 and quality == "P"):
            diatonic_pc_number *= direction
        self._number = diatonic_pc_number

    def _from_number(self, argument):
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
        if self.quality == "P" and abs(self.number) == 1:
            return 0
        return math.sign(self.number)

    @property
    def name(self):
        """
        Gets name of named interval-class.

        ..  container:: example

            >>> abjad.NamedIntervalClass('-M9').name
            '-M2'

        Returns string.
        """
        return "{}{}{}".format(
            _lib._direction_number_to_direction_symbol[self.direction_number],
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
        Makes named interval-class from ``pitch_carrier_1`` and
        ``pitch_carrier_2``

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
        named_interval = NamedInterval.from_pitch_carriers(
            pitch_carrier_1, pitch_carrier_2
        )
        return class_(named_interval)


class NamedInversionEquivalentIntervalClass(NamedIntervalClass):
    """
    Named inversion-equivalent interval-class.

    ..  container:: example

        Initializes from string:

        >>> abjad.NamedInversionEquivalentIntervalClass('-m14')
        NamedInversionEquivalentIntervalClass('+M2')

    ..  container:: example

        Initializes from pair:

        >>> abjad.NamedInversionEquivalentIntervalClass(('perfect', 1))
        NamedInversionEquivalentIntervalClass('P1')

        >>> abjad.NamedInversionEquivalentIntervalClass(('perfect', -1))
        NamedInversionEquivalentIntervalClass('P1')

        >>> abjad.NamedInversionEquivalentIntervalClass(('augmented', 4))
        NamedInversionEquivalentIntervalClass('+A4')

        >>> abjad.NamedInversionEquivalentIntervalClass(('augmented', -4))
        NamedInversionEquivalentIntervalClass('+A4')

        >>> abjad.NamedInversionEquivalentIntervalClass(('augmented', 11))
        NamedInversionEquivalentIntervalClass('+A4')

        >>> abjad.NamedInversionEquivalentIntervalClass(('augmented', -11))
        NamedInversionEquivalentIntervalClass('+A4')

    ..  container:: example

        Initializes from other interval-class:

        >>> interval_class = abjad.NamedInversionEquivalentIntervalClass(
        ...     'P1',
        ...     )
        >>> abjad.NamedInversionEquivalentIntervalClass(interval_class)
        NamedInversionEquivalentIntervalClass('P1')

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, name="P1"):
        super().__init__(name or "P1")
        self._quality, self._number = self._process_quality_and_number(
            self._quality, self._number
        )

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a named inversion-equivalent
        interval-class with name equal to that of this named
        inversion-equivalent interval-class.

        ..  container:: example

            >>> class_ = abjad.NamedInversionEquivalentIntervalClass
            >>> interval_class_1 = class_('P1')
            >>> interval_class_2 = class_('P1')
            >>> interval_class_3 = class_('m2')

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

    def __hash__(self):
        """
        Hashes named inversion-equivalent interval-class.

        Returns integer.
        """
        return super().__hash__()

    ### PRIVATE METHODS ###

    @classmethod
    def _invert_quality_string(class_, quality):
        inversions = {"M": "m", "m": "M", "P": "P"}
        if quality in inversions:
            return inversions[quality]
        if quality[0] == "A":
            return "d" * len(quality)
        return "A" * len(quality)

    @classmethod
    def _is_representative_number(class_, argument):
        if isinstance(argument, numbers.Number):
            if 1 <= argument <= 4 or argument == 8:
                return True
        return False

    @classmethod
    def _process_quality_and_number(class_, quality, number):
        if number == 0:
            raise ValueError("named interval can not equal zero.")
        elif abs(number) == 1:
            number = 1
        elif abs(number) % 7 == 0:
            number = 7
        elif abs(number) % 7 == 1:
            number = 8
        else:
            number = abs(number) % 7
        if class_._is_representative_number(number):
            quality = quality
            number = number
        else:
            quality = class_._invert_quality_string(quality)
            number = 9 - number
        return quality, number

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(class_, pitch_carrier_1, pitch_carrier_2):
        """
        Makes named inversion-equivalent interval-class from
        ``pitch_carrier_1`` and ``pitch_carrier_2``

        ..  container:: example

            >>> class_ = abjad.NamedInversionEquivalentIntervalClass
            >>> class_.from_pitch_carriers(
            ...     abjad.NamedPitch(-2),
            ...     abjad.NamedPitch(12),
            ...     )
            NamedInversionEquivalentIntervalClass('+M2')

        Returns new named inversion-equivalent interval-class.
        """
        named_interval = NamedInterval.from_pitch_carriers(
            pitch_carrier_1, pitch_carrier_2
        )
        string = str(named_interval)
        return class_(string)


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

    __slots__ = ("_number",)

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
        Adds ``argument`` to numbered interval-class.

        Returns new numbered interval-class.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return type(self)(float(self) + float(argument))

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a numbered interval-class with number
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
        Is true when numbered interval-class is less than ``argument``

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

    def __radd__(self, argument):
        """
        Adds ``argument`` to numbered interval-class.

        Returns new numbered interval-class.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return NotImplemented
        return type(self)(float(self) + float(argument))

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
            string = "+" + string
        return string

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from numbered interval-class.

        Returns new numbered interval-class.
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
        self._number = self._named_to_numbered(direction, quality, diatonic_number)

    def _from_number(self, argument):
        direction = math.sign(argument)
        number = self._to_nearest_quarter_tone(abs(argument))
        pc_number = number % 12
        if pc_number == 0 and number:
            pc_number = 12
        self._number = pc_number * direction

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
        """Makes numbered interval-class from ``pitch_carrier_1`` and
        ``pitch_carrier_2``

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
        interval = NumberedInterval.from_pitch_carriers(
            pitch_carrier_1, pitch_carrier_2
        )
        return class_(interval)


class NumberedInversionEquivalentIntervalClass(NumberedIntervalClass):
    """
    Numbered inversion-equivalent interval-class.

    ..  container:: example

        Initializes from integer:

        >>> abjad.NumberedInversionEquivalentIntervalClass(0)
        NumberedInversionEquivalentIntervalClass(0)

        >>> abjad.NumberedInversionEquivalentIntervalClass(1)
        NumberedInversionEquivalentIntervalClass(1)

    ..  container:: example

        Initializes from float:

        >>> abjad.NumberedInversionEquivalentIntervalClass(1.5)
        NumberedInversionEquivalentIntervalClass(1.5)

    ..  container:: example

        Initializes from string:

        >>> abjad.NumberedInversionEquivalentIntervalClass('1')
        NumberedInversionEquivalentIntervalClass(1)

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, number=0):
        super().__init__(number or 0)
        self._number %= 12
        if 6 < self._number:
            self._number = 12 - self._number

    ### SPECIAL METHODS ###

    def __abs__(self):
        """
        Gets absolute value of numbered inversion-equivalent
        interval-class.

        ..  container:: example

            >>> abs(abjad.NumberedInversionEquivalentIntervalClass(0))
            NumberedInversionEquivalentIntervalClass(0)

            >>> abs(abjad.NumberedInversionEquivalentIntervalClass(1.5))
            NumberedInversionEquivalentIntervalClass(1.5)

        Returns new numbered inversion-equivalent interval-class.
        """
        return type(self)(abs(self.number))

    def __lt__(self, argument):
        """
        Is true when ``argument`` is a numbered inversion-equivalent
        interval-class with a number less than this numbered
        inversion-equivalent interval-class.
        """
        if isinstance(argument, type(self)):
            return self.number < argument.number
        return False

    def __neg__(self):
        """
        Negates numbered inversion-equivalent interval-class.

        ..  container:: example

            >>> -abjad.NumberedInversionEquivalentIntervalClass(0)
            NumberedInversionEquivalentIntervalClass(0)

            >>> -abjad.NumberedInversionEquivalentIntervalClass(1.5)
            NumberedInversionEquivalentIntervalClass(1.5)

        Returns new numbered inversion-equivalent interval-class.
        """
        return type(self)(self.number)

    def __str__(self):
        """
        Gets string representation of numbered inversion-equivalent
        interval-class.

        ..  container:: example

            >>> str(abjad.NumberedInversionEquivalentIntervalClass(0))
            '0'

            >>> str(abjad.NumberedInversionEquivalentIntervalClass(1.5))
            '1.5'

        Returns string.
        """
        return str(self.number)
