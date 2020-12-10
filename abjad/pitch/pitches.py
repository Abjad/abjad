import functools
import math
import numbers
import typing

import quicktions

from .. import math as _math
from ..storage import FormatSpecification, StorageFormatManager
from . import _lib
from .Accidental import Accidental
from .Octave import Octave


@functools.total_ordering
class Pitch:
    """
    Abstract pitch.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_pitch_class", "_octave")

    _is_abstract = True

    ### INITIALIZER ###

    def __init__(self, argument, accidental=None, arrow=None, octave=None):
        from .pitchclasses import NamedPitchClass, PitchClass

        if isinstance(argument, str):
            match = _lib._comprehensive_pitch_name_regex.match(argument)
            if not match:
                match = _lib._comprehensive_pitch_class_name_regex.match(argument)
            if not match:
                class_name = type(self).__name__
                message = f"can not instantiate {class_name} from {argument!r}."
                raise ValueError(message)
            group_dict = match.groupdict()
            _dpc_name = group_dict["diatonic_pc_name"].lower()
            _dpc_number = _lib._diatonic_pc_name_to_diatonic_pc_number[_dpc_name]
            _alteration = Accidental(group_dict["comprehensive_accidental"]).semitones
            _octave = Octave(group_dict.get("comprehensive_octave", "")).number
            self._from_named_parts(_dpc_number, _alteration, _octave)
        elif isinstance(argument, numbers.Number):
            self._from_number(argument)
        elif isinstance(argument, (Pitch, PitchClass)):
            self._from_pitch_or_pitch_class(argument)
        elif isinstance(argument, tuple) and len(argument) == 2:
            _pitch_class = NamedPitchClass(argument[0])
            _octave = Octave(argument[1])
            self._from_named_parts(
                _pitch_class._get_diatonic_pc_number(),
                _pitch_class._get_alteration(),
                _octave.number,
            )
        elif hasattr(argument, "written_pitch"):
            self._from_pitch_or_pitch_class(argument.written_pitch)
        elif hasattr(argument, "note_heads") and len(argument.note_heads):
            self._from_pitch_or_pitch_class(argument.note_heads[0])
        else:
            class_name = type(self).__name__
            raise ValueError(f"can not instantiate {class_name} from {argument!r}.")
        if accidental is not None:
            accidental = Accidental(accidental)
            self._pitch_class = type(self._pitch_class)(
                self._pitch_class, accidental=accidental
            )
        if arrow is not None:
            self._pitch_class = type(self._pitch_class)(self._pitch_class, arrow=arrow)
        if octave is not None:
            octave = Octave(octave)
            self._octave = octave

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __float__(self):
        """
        Coerce to float.

        Returns float.
        """
        return float(self.number)

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
        Is true when pitch is less than ``argument``.

        Returns true or false.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE PROPERTIES ###

    def _get_lilypond_format(self):
        raise NotImplementedError

    @staticmethod
    def _to_nearest_octave(pitch_number, pitch_class_number):
        target_pc = pitch_number % 12
        down = (target_pc - pitch_class_number) % 12
        up = (pitch_class_number - target_pc) % 12
        if up < down:
            return pitch_number + up
        else:
            return pitch_number - down

    @staticmethod
    def _to_nearest_quarter_tone(number):
        number = round(float(number) * 4) / 4
        quotient, remainder = divmod(number, 1)
        if remainder == 0.75:
            quotient += 1
        elif remainder == 0.5:
            quotient += 0.5
        return _math.integer_equivalent_number_to_integer(quotient)

    @staticmethod
    def _to_pitch_class_item_class(item_class):
        from .pitchclasses import NamedPitchClass, NumberedPitchClass

        item_class = item_class or NumberedPitch
        if item_class in (NamedPitchClass, NumberedPitchClass):
            return item_class
        elif item_class is NamedPitch:
            return NamedPitchClass
        elif item_class is NumberedPitch:
            return NumberedPitchClass
        else:
            raise TypeError(item_class)

    @staticmethod
    def _to_pitch_item_class(item_class):
        from .pitchclasses import NamedPitchClass, NumberedPitchClass

        item_class = item_class or NumberedPitch
        if item_class in (NamedPitch, NumberedPitch):
            return item_class
        elif item_class is NamedPitchClass:
            return NamedPitch
        elif item_class is NumberedPitchClass:
            return NumberedPitch
        else:
            raise TypeError(item_class)

    ### PUBLIC PROPERTIES ###

    @property
    def arrow(self):
        """
        Gets arrow of pitch.
        """
        raise NotImplementedError

    @property
    def hertz(self):
        """
        Gets frequency of pitch in Hertz.

        Returns float.
        """
        hertz = pow(2.0, (float(self.number) - 9.0) / 12.0) * 440.0
        return hertz

    @property
    def name(self):
        """
        Gets name of pitch.

        Returns string.
        """
        raise NotImplementedError

    @property
    def number(self):
        """
        Gets number of pitch.

        Returns number.
        """
        raise NotImplementedError

    @property
    def octave(self):
        """
        Gets octave of pitch.

        Returns octave.
        """
        raise NotImplementedError

    @property
    def pitch_class(self):
        """
        Gets pitch-class of pitch.

        Returns pitch-class.
        """
        raise NotImplementedError

    ### PUBLIC METHODS ###

    @classmethod
    def from_hertz(class_, hertz):
        """
        Creates pitch from ``hertz``.

        Returns new pitch.
        """
        midi = 9.0 + (12.0 * math.log(float(hertz) / 440.0, 2))
        pitch = class_(midi)
        return pitch

    def get_name(self, locale=None):
        """
        Gets name of pitch according to ``locale``.

        Returns string.
        """
        raise NotImplementedError

    def invert(self, axis=None):
        """
        Inverts pitch about ``axis``.

        Interprets ``axis`` of none equal to middle C.

        Returns new pitch.
        """
        axis = axis or NamedPitch("c'")
        axis = type(self)(axis)
        interval = self - axis
        result = axis.transpose(interval)
        return result

    def multiply(self, n=1):
        """
        Multiplies pitch by ``n``.

        Returns new pitch.
        """
        return type(self)(n * self.number)

    def transpose(self, n):
        """
        Transposes pitch by index ``n``.

        Returns new pitch.
        """
        raise NotImplementedError


### TYPINGS ###

PitchTyping = typing.Union[int, str, Pitch]


class NamedPitch(Pitch):
    r"""
    Named pitch.

    ..  container:: example

        Initializes from pitch name:

        >>> abjad.NamedPitch("cs''")
        NamedPitch("cs''")

        Initializes quartertone from pitch name:

        >>> abjad.NamedPitch("aqs")
        NamedPitch('aqs')

    ..  container:: example

        Initializes from pitch-class / octave string:

        >>> abjad.NamedPitch('C#5')
        NamedPitch("cs''")

        Initializes quartertone from pitch-class / octave string:

        >>> abjad.NamedPitch('A+3')
        NamedPitch('aqs')

        >>> abjad.NamedPitch('Aqs3')
        NamedPitch('aqs')

    ..  container:: example

        Initializes arrowed pitch:

        >>> abjad.NamedPitch('C#5', arrow=abjad.Up)
        NamedPitch("cs''", arrow=Up)

    ..  container:: example

        REGRESSION. Small floats just less than a C initialize in the correct
        octave.

        Initializes c / C3:

        >>> abjad.NamedPitch(-12.1)
        NamedPitch('c')

        Initializes c' / C4:

        >>> abjad.NamedPitch(-0.1)
        NamedPitch("c'")

        Initializes c'' / C5:

        >>> abjad.NamedPitch(11.9)
        NamedPitch("c''")

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, name="c'", *, accidental=None, arrow=None, octave=None):
        super().__init__(
            name or "c'", accidental=accidental, arrow=arrow, octave=octave
        )

    ### SPECIAL METHODS ###

    def __add__(self, interval):
        """
        Adds named pitch to ``interval``.

        ..  container:: example

            >>> abjad.NamedPitch("cs''") + abjad.NamedInterval('-M2')
            NamedPitch("b'")

            >>> abjad.NamedPitch("cs''") + abjad.NamedInterval('P1')
            NamedPitch("cs''")

            >>> abjad.NamedPitch("cs''") + abjad.NamedInterval('+M2')
            NamedPitch("ds''")

        Returns new named pitch.
        """
        from .intervals import NamedInterval

        interval = NamedInterval(interval)
        return interval.transpose(self)

    def __copy__(self, *arguments):
        """
        Copies named pitch.

        >>> import copy

        ..  container:: example

            >>> copy.copy(abjad.NamedPitch("c''"))
            NamedPitch("c''")

            >>> copy.copy(abjad.NamedPitch("cs''"))
            NamedPitch("cs''")

            >>> copy.copy(abjad.NamedPitch("df''"))
            NamedPitch("df''")

        ..  container:: example

            Copies arrowed pitch:

            >>> pitch = abjad.NamedPitch("cs''", arrow=abjad.Up)
            >>> copy.copy(pitch)
            NamedPitch("cs''", arrow=Up)

        Returns new named pitch.
        """
        return type(self)(self, arrow=self.arrow)

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a named pitch equal to this named pitch.

        ..  container:: example

            >>> pitch_1 = abjad.NamedPitch('fs')
            >>> pitch_2 = abjad.NamedPitch('fs')
            >>> pitch_3 = abjad.NamedPitch('gf')

            >>> pitch_1 == pitch_1
            True
            >>> pitch_1 == pitch_2
            True
            >>> pitch_1 == pitch_3
            False

            >>> pitch_2 == pitch_1
            True
            >>> pitch_2 == pitch_2
            True
            >>> pitch_2 == pitch_3
            False

            >>> pitch_3 == pitch_1
            False
            >>> pitch_3 == pitch_2
            False
            >>> pitch_3 == pitch_3
            True

        Returns true or false.
        """
        return super().__eq__(argument)

    def __hash__(self):
        """
        Hashes named pitch.

        Returns integer.
        """
        return super().__hash__()

    def __lt__(self, argument):
        """
        Is true when named pitch is less than ``argument``.

        ..  container:: example

            >>> pitch_1 = abjad.NamedPitch('fs')
            >>> pitch_2 = abjad.NamedPitch('fs')
            >>> pitch_3 = abjad.NamedPitch('gf')

            >>> pitch_1 < pitch_1
            False
            >>> pitch_1 < pitch_2
            False
            >>> pitch_1 < pitch_3
            True

            >>> pitch_2 < pitch_1
            False
            >>> pitch_2 < pitch_2
            False
            >>> pitch_2 < pitch_3
            True

            >>> pitch_3 < pitch_1
            False
            >>> pitch_3 < pitch_2
            False
            >>> pitch_3 < pitch_3
            False

        Returns true or false.
        """
        try:
            argument = type(self)(argument)
        except (TypeError, ValueError):
            return False
        self_dpn = self._get_diatonic_pitch_number()
        argument_dpn = argument._get_diatonic_pitch_number()
        if self_dpn == argument_dpn:
            return self.accidental < argument.accidental
        return self_dpn < argument_dpn

    def __radd__(self, interval):
        """
        Right-addition not defined on named pitches.

        ..  container:: example

            >>> abjad.NamedPitch("cs'").__radd__(1)
            Traceback (most recent call last):
                ...
            NotImplementedError: right-addition not defined on NamedPitch.

        """
        message = f"right-addition not defined on {type(self).__name__}."
        raise NotImplementedError(message)

    def __str__(self):
        """
        Gets string representation of named pitch.

        ..  container:: example

            >>> str(abjad.NamedPitch("c''"))
            "c''"

            >>> str(abjad.NamedPitch("cs''"))
            "cs''"

            >>> str(abjad.NamedPitch("df''"))
            "df''"

        Returns string.
        """
        return self.name

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("cs''") - abjad.NamedPitch("b'")
            NamedInterval('-M2')

            >>> abjad.NamedPitch("cs''") - abjad.NamedPitch("fs''")
            NamedInterval('+P4')

        Returns named interval.
        """
        from .intervals import NamedInterval

        if isinstance(argument, type(self)):
            return NamedInterval.from_pitch_carriers(self, argument)
        interval = NamedInterval(argument)
        interval = -interval
        return interval.transpose(self)

    ### PRIVATE METHODS ###

    def _apply_accidental(self, accidental):
        name = self._get_diatonic_pc_name()
        name += str(self.accidental + Accidental(accidental))
        name += self.octave.ticks
        return type(self)(name)

    def _from_named_parts(self, dpc_number, alteration, octave):
        from .pitchclasses import NamedPitchClass

        dpc_name = _lib._diatonic_pc_number_to_diatonic_pc_name[dpc_number]
        accidental = Accidental(alteration)
        octave = Octave(octave)
        self._octave = octave
        self._pitch_class = NamedPitchClass(dpc_name + str(accidental))

    def _from_number(self, number):
        from .pitchclasses import NumberedPitchClass

        number = self._to_nearest_quarter_tone(number)
        quotient, remainder = divmod(number, 12)
        pitch_class = NumberedPitchClass(remainder)
        self._from_named_parts(
            dpc_number=pitch_class._get_diatonic_pc_number(),
            alteration=pitch_class._get_alteration(),
            octave=quotient + 4,
        )

    def _from_pitch_or_pitch_class(self, pitch_or_pitch_class):
        from .pitchclasses import NamedPitchClass

        name = pitch_or_pitch_class._get_lilypond_format()
        if not isinstance(pitch_or_pitch_class, Pitch):
            name += "'"
        if isinstance(pitch_or_pitch_class, Pitch):
            self._pitch_class = NamedPitchClass(pitch_or_pitch_class.pitch_class)
            self._octave = pitch_or_pitch_class.octave
        else:
            self._pitch_class = NamedPitchClass(pitch_or_pitch_class)
            self._octave = Octave()

    def _get_alteration(self):
        return self.accidental.semitones

    def _get_diatonic_pc_name(self):
        return _lib._diatonic_pc_number_to_diatonic_pc_name[
            self.pitch_class._diatonic_pc_number
        ]

    def _get_diatonic_pc_number(self):
        diatonic_pc_name = self._get_diatonic_pc_name()
        diatonic_pc_number = _lib._diatonic_pc_name_to_diatonic_pc_number[
            diatonic_pc_name
        ]
        return diatonic_pc_number

    def _get_diatonic_pitch_number(self):
        diatonic_pitch_number = 7 * (self.octave.number - 4)
        diatonic_pitch_number += self._get_diatonic_pc_number()
        return diatonic_pitch_number

    def _get_format_specification(self):
        return FormatSpecification(
            self,
            coerce_for_equality=True,
            repr_is_indented=False,
            storage_format_args_values=[self.name],
            storage_format_is_indented=False,
            storage_format_keyword_names=["arrow"],
        )

    def _get_lilypond_format(self):
        return str(self)

    def _list_format_contributions(self):
        contributions = []
        if self.arrow is None:
            return contributions
        string = r"\once \override Accidental.stencil ="
        string += " #ly:text-interface::print"
        contributions.append(string)
        glyph = f"accidentals.{self.accidental.name}"
        glyph += f".arrow{str(self.arrow).lower()}"
        string = r"\once \override Accidental.text ="
        string += rf' \markup {{ \musicglyph #"{glyph}" }}'
        contributions.append(string)
        return contributions

    def _respell(self, accidental="sharps"):
        if accidental == "sharps":
            dictionary = _lib._pitch_class_number_to_pitch_class_name_with_sharps
        else:
            assert accidental == "flats"
            dictionary = _lib._pitch_class_number_to_pitch_class_name_with_flats
        name = dictionary[self.pitch_class.number]
        candidate = type(self)((name, self.octave.number))
        if candidate.number == self.number - 12:
            candidate = type(self)(candidate, octave=candidate.octave.number + 1)
        elif candidate.number == self.number + 12:
            candidate = type(self)(candidate, octave=candidate.octave.number - 1)
        assert candidate.number == self.number
        return candidate

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        """
        Gets accidental of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").accidental
            Accidental('natural')

            >>> abjad.NamedPitch("cs''").accidental
            Accidental('sharp')

            >>> abjad.NamedPitch("df''").accidental
            Accidental('flat')

        Returns accidental.
        """
        return self.pitch_class.accidental

    @property
    def arrow(self):
        """
        Gets arrow of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("cs''").arrow is None
            True

            >>> abjad.NamedPitch("cs''", arrow=abjad.Up).arrow
            Up

            >>> abjad.NamedPitch("cs''", arrow=abjad.Down).arrow
            Down

        ..  container:: example

            Displays arrow in interpreter representation:

            >>> abjad.NamedPitch("cs''", arrow=abjad.Down)
            NamedPitch("cs''", arrow=Down)

        Returns up, down or none.
        """
        return self._pitch_class.arrow

    @property
    def hertz(self):
        """
        Gets frequency of named pitch in Hertz.

        ..  container:: example

            >>> abjad.NamedPitch("c''").hertz
            523.25...

            >>> abjad.NamedPitch("cs''").hertz
            554.36...

            >>> abjad.NamedPitch("df''").hertz
            554.36...

        Returns float.
        """
        return super().hertz

    @property
    def name(self):
        """
        Gets name of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").name
            "c''"

            >>> abjad.NamedPitch("cs''").name
            "cs''"

            >>> abjad.NamedPitch("df''").name
            "df''"

        Returns string.
        """
        return f"{self.pitch_class!s}{self.octave!s}"

    @property
    def number(self):
        """
        Gets number of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").number
            12

            >>> abjad.NamedPitch("cs''").number
            13

            >>> abjad.NamedPitch("df''").number
            13

            >>> abjad.NamedPitch("cf'").number
            -1

        Returns number.
        """
        diatonic_pc_number = self.pitch_class._get_diatonic_pc_number()
        pc_number = _lib._diatonic_pc_number_to_pitch_class_number[diatonic_pc_number]
        alteration = self.pitch_class._get_alteration()
        octave_base_pitch = (self.octave.number - 4) * 12
        return _math.integer_equivalent_number_to_integer(
            pc_number + alteration + octave_base_pitch
        )

    @property
    def octave(self):
        """
        Gets octave of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").octave
            Octave(5)

            >>> abjad.NamedPitch("cs''").octave
            Octave(5)

            >>> abjad.NamedPitch("df''").octave
            Octave(5)

        Returns octave.
        """
        return self._octave

    @property
    def pitch_class(self):
        """
        Gets pitch-class of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").pitch_class
            NamedPitchClass('c')

            >>> abjad.NamedPitch("cs''").pitch_class
            NamedPitchClass('cs')

            >>> abjad.NamedPitch("df''").pitch_class
            NamedPitchClass('df')

        Returns named pitch-class.
        """
        return self._pitch_class

    ### PUBLIC METHODS ###

    @classmethod
    def from_hertz(class_, hertz):
        """
        Makes named pitch from ``hertz``.

        ..  container:: example

            >>> abjad.NamedPitch.from_hertz(440)
            NamedPitch("a'")

        ..  container:: example

            REGRESSION. Returns c'' (C5) and not c' (C4):

            >>> abjad.NamedPitch.from_hertz(519)
            NamedPitch("c''")

        Returns newly constructed named pitch.
        """
        return super().from_hertz(hertz)

    def get_name(self, locale=None):
        """
        Gets name of named pitch according to ``locale``.

        ..  container:: example

            >>> abjad.NamedPitch("cs''").get_name()
            "cs''"

            >>> abjad.NamedPitch("cs''").get_name(locale='us')
            'C#5'

        Set ``locale`` to ``'us'`` or none.

        Returns string.
        """
        if locale is None:
            return self.name
        elif locale == "us":
            name = self._get_diatonic_pc_name().upper()
            return f"{name}{self.accidental.symbol}{self.octave.number}"
        else:
            raise ValueError(f"must be 'us' or none: {locale!r}.")

    def invert(self, axis=None):
        """
        Inverts named pitch around ``axis``.

        ..  container:: example

            Inverts pitch around middle C explicitly:

            >>> abjad.NamedPitch("d'").invert("c'")
            NamedPitch('bf')

            >>> abjad.NamedPitch('bf').invert("c'")
            NamedPitch("d'")

        ..  container:: example

            Inverts pitch around middle C implicitly:

            >>> abjad.NamedPitch("d'").invert()
            NamedPitch('bf')

            >>> abjad.NamedPitch('bf').invert()
            NamedPitch("d'")

        ..  container:: example

            Inverts pitch around A3:

            >>> abjad.NamedPitch("d'").invert('a')
            NamedPitch('e')

        Interprets none-valued ``axis`` equal to middle C.

        Returns new named pitch.
        """
        return super().invert(axis=axis)

    def multiply(self, n=1):
        """
        Multiplies named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("d'").multiply(1)
            NamedPitch("d'")

            >>> abjad.NamedPitch("d'").multiply(3)
            NamedPitch("fs'")

            >>> abjad.NamedPitch("d'").multiply(6)
            NamedPitch("c''")

            >>> abjad.NamedPitch("d'").multiply(6.5)
            NamedPitch("cs''")

        Returns new named pitch.
        """
        return super().multiply(n=n)

    def simplify(self):
        """
        Reduce alteration to between -2 and 2 while maintaining identical pitch
        number.

            >>> abjad.NamedPitch("cssqs'").simplify()
            NamedPitch("dqs'")

            >>> abjad.NamedPitch("cfffqf'").simplify()
            NamedPitch('aqf')

            >>> float(abjad.NamedPitch("cfffqf'").simplify()) == float(abjad.NamedPitch('aqf'))
            True

        ..  note:: LilyPond by default only supports accidentals from
                   double-flat to double-sharp.

        Returns named pitch.
        """
        alteration = self._get_alteration()
        if abs(alteration) <= 2:
            return self
        diatonic_pc_number = self._get_diatonic_pc_number()
        octave = int(self.octave)
        while alteration > 2:
            step_size = 2
            if diatonic_pc_number == 2:  # e to f
                step_size = 1
            elif diatonic_pc_number == 6:  # b to c
                step_size = 1
                octave += 1
            diatonic_pc_number = (diatonic_pc_number + 1) % 7
            alteration -= step_size
        while alteration < -2:
            step_size = 2
            if diatonic_pc_number == 3:  # f to e
                step_size = 1
            elif diatonic_pc_number == 0:  # c to b
                step_size = 1
                octave -= 1
            diatonic_pc_number = (diatonic_pc_number - 1) % 7
            alteration += step_size
        diatonic_pc_name = _lib._diatonic_pc_number_to_diatonic_pc_name[
            diatonic_pc_number
        ]
        accidental = Accidental(alteration)
        octave = Octave(octave)
        pitch_name = f"{diatonic_pc_name}{accidental!s}{octave!s}"
        return type(self)(pitch_name, arrow=self.arrow)

    def transpose(self, n=0):
        """
        Transposes named pitch by index ``n``.

        ..  container:: example

            Transposes C4 up a minor second:

            >>> abjad.NamedPitch("c'").transpose(n='m2')
            NamedPitch("df'")

        ..  container:: example

            Transposes C4 down a major second:

            >>> abjad.NamedPitch("c'").transpose(n='-M2')
            NamedPitch('bf')

        Returns new named pitch.
        """
        from .intervals import NamedInterval

        interval = NamedInterval(n)
        pitch_number = self.number + interval.semitones
        diatonic_pc_number = self._get_diatonic_pc_number()
        diatonic_pc_number += interval.staff_spaces
        diatonic_pc_number %= 7
        diatonic_pc_name = _lib._diatonic_pc_number_to_diatonic_pc_name[
            diatonic_pc_number
        ]
        pc = _lib._diatonic_pc_name_to_pitch_class_number[diatonic_pc_name]
        nearest_neighbor = self._to_nearest_octave(pitch_number, pc)
        semitones = pitch_number - nearest_neighbor
        accidental = Accidental(semitones)
        octave = int(math.floor((pitch_number - semitones) / 12)) + 4
        octave = Octave(octave)
        name = diatonic_pc_name + str(accidental) + octave.ticks
        return type(self)(name)


class NumberedPitch(Pitch):
    r"""
    Numbered pitch.

    ..  container:: example

        Initializes from number:

        >>> abjad.NumberedPitch(13)
        NumberedPitch(13)

    ..  container:: example

        Initializes from other numbered pitch

        >>> abjad.NumberedPitch(abjad.NumberedPitch(13))
        NumberedPitch(13)

    ..  container:: example

        Initializes from pitch-class / octave pair:

        >>> abjad.NumberedPitch((1, 5))
        NumberedPitch(13)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_number",)

    ### INITIALIZER ###

    def __init__(self, number=0, *, arrow=None, octave=None):
        super().__init__(number or 0, arrow=arrow, octave=octave)

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        """
        Adds ``argument`` to numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(12) + abjad.NumberedPitch(13)
            NumberedPitch(25)

            >>> abjad.NumberedPitch(13) + abjad.NumberedPitch(12)
            NumberedPitch(25)

        Returns new numbered pitch.
        """
        argument = type(self)(argument)
        semitones = float(self) + float(argument)
        return type(self)(semitones)

    def __lt__(self, argument):
        r"""Is true when ``argument`` can be coerced to a numbered pitch and when this
        numbered pitch is less than ``argument``.

        ..  container:: example

            >>> pitch_1 = abjad.NumberedPitch(12)
            >>> pitch_2 = abjad.NumberedPitch(12)
            >>> pitch_3 = abjad.NumberedPitch(13)

            >>> pitch_1 < pitch_1
            False
            >>> pitch_1 < pitch_2
            False
            >>> pitch_1 < pitch_3
            True

            >>> pitch_2 < pitch_1
            False
            >>> pitch_2 < pitch_2
            False
            >>> pitch_2 < pitch_3
            True

            >>> pitch_3 < pitch_1
            False
            >>> pitch_3 < pitch_2
            False
            >>> pitch_3 < pitch_3
            False

        Returns true or false.
        """
        try:
            argument = type(self)(argument)
        except (ValueError, TypeError):
            return False
        return self.number < argument.number

    def __neg__(self):
        """
        Negates numbered pitch.

        ..  container:: example

            >>> -abjad.NumberedPitch(13.5)
            NumberedPitch(-13.5)

            >>> -abjad.NumberedPitch(-13.5)
            NumberedPitch(13.5)

        Returns new numbered pitch.
        """
        return type(self)(-self.number)

    def __radd__(self, argument):
        """
        Adds numbered pitch to ``argument``.

        ..  container:: example

            >>> pitch = abjad.NumberedPitch(13)
            >>> abjad.NumberedPitch(12).__radd__(pitch)
            NumberedPitch(25)

            >>> pitch = abjad.NumberedPitch(12)
            >>> abjad.NumberedPitch(13).__radd__(pitch)
            NumberedPitch(25)

        Returns new numbered pitch.
        """
        argument = type(self)(argument)
        return argument.__add__(self)

    def __str__(self):
        """
        Gets string representation of numbered pitch.

        Returns string.
        """
        return str(self.number)

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(12) - abjad.NumberedPitch(12)
            NumberedInterval(0)

            >>> abjad.NumberedPitch(12) - abjad.NumberedPitch(13)
            NumberedInterval(1)

            >>> abjad.NumberedPitch(13) - abjad.NumberedPitch(12)
            NumberedInterval(-1)

        Returns numbered interval.
        """
        from .intervals import NumberedInterval

        if isinstance(argument, type(self)):
            return NumberedInterval.from_pitch_carriers(self, argument)
        interval = NumberedInterval(argument)
        interval = -interval
        return interval.transpose(self)

    ### PRIVATE METHODS ###

    def _apply_accidental(self, accidental=None):
        accidental = Accidental(accidental)
        semitones = self.number + accidental.semitones
        return type(self)(semitones)

    def _from_named_parts(self, dpc_number, alteration, octave):
        from .pitchclasses import NumberedPitchClass

        pc_number = _lib._diatonic_pc_number_to_pitch_class_number[dpc_number]
        pc_number += alteration
        pc_number += (octave - 4) * 12
        self._number = _math.integer_equivalent_number_to_integer(pc_number)
        octave_number, pc_number = divmod(self._number, 12)
        self._pitch_class = NumberedPitchClass(pc_number)
        self._octave = Octave(octave_number + 4)

    def _from_number(self, number):
        from .pitchclasses import NumberedPitchClass

        self._number = self._to_nearest_quarter_tone(number)
        octave_number, pc_number = divmod(self._number, 12)
        self._octave = Octave(octave_number + 4)
        self._pitch_class = NumberedPitchClass(pc_number)

    def _from_pitch_or_pitch_class(self, pitch_or_pitch_class):
        from .pitchclasses import NumberedPitchClass

        self._number = self._to_nearest_quarter_tone(float(pitch_or_pitch_class))
        octave_number, pc_number = divmod(self._number, 12)
        self._octave = Octave(octave_number + 4)
        self._pitch_class = NumberedPitchClass(
            pc_number, arrow=pitch_or_pitch_class.arrow
        )

    def _get_diatonic_pc_name(self):
        return self.pitch_class._get_diatonic_pc_name()

    def _get_diatonic_pc_number(self):
        return self.numbered_pitch_class._get_diatonic_pc_number()

    def _get_diatonic_pitch_number(self):
        result = 7 * (self.octave.number - 4)
        result += self._get_diatonic_pc_number()
        return result

    def _get_format_specification(self):
        return FormatSpecification(
            client=self,
            coerce_for_equality=True,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=[self.number],
            storage_format_keyword_names=["arrow"],
        )

    def _get_lilypond_format(self):
        return self.name

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        """
        Gets accidental of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitchClass(13).accidental
            Accidental('sharp')

        Returns accidental.
        """
        return self.pitch_class.accidental

    @property
    def arrow(self):
        """
        Gets arrow of numbered pitch.

        ..  container:: example

            Gets no arrow:

            >>> abjad.NumberedPitch(13).arrow is None
            True

        ..  container:: example

            Gets up-arrow:

            >>> abjad.NumberedPitch(13, arrow=abjad.Up).arrow
            Up

        ..  container:: example

            Gets down-arrow:

            >>> abjad.NumberedPitch(13, arrow=abjad.Down).arrow
            Down

        Returns up, down or none.
        """
        return self._pitch_class.arrow

    @property
    def hertz(self):
        """
        Gets frequency of numbered pitch in Hertz.

        ..  container:: example

            >>> abjad.NumberedPitch(9).hertz
            440.0

            >>> abjad.NumberedPitch(0).hertz
            261.62...

            >>> abjad.NumberedPitch(12).hertz
            523.25...

        Returns float.
        """
        return super().hertz

    @property
    def name(self):
        """
        Gets name of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(13).name
            "cs''"

        Returns string
        """
        return f"{self.pitch_class.name}{self.octave.ticks}"

    @property
    def number(self):
        """
        Gets number of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(13).number
            13

        Returns number.
        """
        pc_number = float(self.pitch_class)
        octave_base_pitch = (self.octave.number - 4) * 12
        return _math.integer_equivalent_number_to_integer(pc_number + octave_base_pitch)

    @property
    def octave(self):
        """
        Gets octave of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(13).octave
            Octave(5)

        Returns octave.
        """
        return self._octave

    @property
    def pitch_class(self):
        """
        Gets pitch-class of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(13).pitch_class
            NumberedPitchClass(1)

        Returns numbered pitch-class.
        """
        return self._pitch_class

    ### PUBLIC METHODS ###

    @classmethod
    def from_hertz(class_, hertz):
        """
        Makes numbered pitch from ``hertz``.

        ..  container:: example

            >>> abjad.NumberedPitch.from_hertz(440)
            NumberedPitch(9)

        ..  container:: example

            REGRESSION. Returns 12 (not 0):

            >>> abjad.NumberedPitch.from_hertz(519)
            NumberedPitch(12)

        Returns newly constructed numbered pitch.
        """
        return super().from_hertz(hertz)

    def get_name(self, locale=None):
        """
        Gets name of numbered pitch name according to ``locale``.

        ..  container:: example

            >>> abjad.NumberedPitch(13).get_name()
            "cs''"

            >>> abjad.NumberedPitch(13).get_name(locale='us')
            'C#5'

        Set ``locale`` to ``'us'`` or none.

        Returns string.
        """
        return NamedPitch(self).get_name(locale=locale)

    def interpolate(self, stop_pitch, fraction):
        """
        Interpolates between numbered pitch and ``stop_pitch`` by ``fraction``.

        ..  container:: example

            Interpolates from C4 to C5:

            >>> start_pitch = abjad.NumberedPitch(0)
            >>> stop_pitch = abjad.NumberedPitch(12)

            >>> start_pitch.interpolate(stop_pitch, 0)
            NumberedPitch(0)
            >>> start_pitch.interpolate(stop_pitch, (1, 4))
            NumberedPitch(3)
            >>> start_pitch.interpolate(stop_pitch, (1, 2))
            NumberedPitch(6)
            >>> start_pitch.interpolate(stop_pitch, (3, 4))
            NumberedPitch(9)
            >>> start_pitch.interpolate(stop_pitch, 1)
            NumberedPitch(12)

        ..  container:: example

            Interpolates from C5 to C4:

            >>> start_pitch = abjad.NumberedPitch(12)
            >>> stop_pitch = abjad.NumberedPitch(0)

            >>> start_pitch.interpolate(stop_pitch, 0)
            NumberedPitch(12)
            >>> start_pitch.interpolate(stop_pitch, (1, 4))
            NumberedPitch(9)
            >>> start_pitch.interpolate(stop_pitch, (1, 2))
            NumberedPitch(6)
            >>> start_pitch.interpolate(stop_pitch, (3, 4))
            NumberedPitch(3)
            >>> start_pitch.interpolate(stop_pitch, 1)
            NumberedPitch(0)

        Returns new numbered pitch.
        """
        try:
            fraction = quicktions.Fraction(*fraction)
        except TypeError:
            fraction = quicktions.Fraction(fraction)
        assert 0 <= fraction <= 1, repr(fraction)
        stop_pitch = type(self)(stop_pitch)
        distance = stop_pitch - self
        distance = abs(distance.semitones)
        distance = fraction * distance
        distance = int(distance)
        if stop_pitch < self:
            distance *= -1
        pitch_number = self.number
        pitch_number = pitch_number + distance
        pitch = NumberedPitch(pitch_number)
        if self <= stop_pitch:
            triple = (self, pitch, stop_pitch)
            assert self <= pitch <= stop_pitch, triple
        else:
            triple = (self, pitch, stop_pitch)
            assert self >= pitch >= stop_pitch, triple
        return pitch

    def invert(self, axis=None):
        """
        Inverts numbered pitch around ``axis``.

        ..  container:: example

            Inverts pitch-class about pitch-class 0 explicitly:

            >>> abjad.NumberedPitch(2).invert(0)
            NumberedPitch(-2)

            >>> abjad.NumberedPitch(-2).invert(0)
            NumberedPitch(2)

        ..  container:: example

            Inverts pitch-class about pitch-class 0 implicitly:

            >>> abjad.NumberedPitch(2).invert()
            NumberedPitch(-2)

            >>> abjad.NumberedPitch(-2).invert()
            NumberedPitch(2)

        ..  container:: example

            Inverts pitch-class about pitch-class -3:

            >>> abjad.NumberedPitch(2).invert(-3)
            NumberedPitch(-8)

        Returns new numbered pitch.
        """
        return Pitch.invert(self, axis=axis)

    def multiply(self, n=1):
        """
        Multiplies numbered pitch by index ``n``.

        ..  container:: example

            >>> abjad.NumberedPitch(14).multiply(3)
            NumberedPitch(42)

        Returns new numbered pitch.
        """
        return super().multiply(n=n)

    def transpose(self, n=0):
        """
        Tranposes numbered pitch by ``n`` semitones.

        ..  container:: example

            >>> abjad.NumberedPitch(13).transpose(1)
            NumberedPitch(14)

        Returns new numbered pitch.
        """
        from .intervals import NumberedInterval

        interval = NumberedInterval(n)
        return type(self)(float(self) + float(interval))
