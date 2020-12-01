import functools
import numbers

from .. import enums, math
from ..storage import FormatSpecification, StorageFormatManager
from . import _lib
from .Accidental import Accidental
from .pitches import NamedPitch, NumberedPitch, Pitch


@functools.total_ordering
class PitchClass:
    """
    Abstract pitch-class.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _is_abstract = True

    ### INITIALIZER ###

    def __init__(self, argument):
        if isinstance(argument, str):
            match = _lib._comprehensive_pitch_name_regex.match(argument)
            if not match:
                match = _lib._comprehensive_pitch_class_name_regex.match(argument)
            if not match:
                class_name = type(self).__name__
                message = f"can not instantiate {class_name} from {argument!r}."
                raise ValueError(message)
            group_dict = match.groupdict()
            dpc_name = group_dict["diatonic_pc_name"].lower()
            dpc_number = _lib._diatonic_pc_name_to_diatonic_pc_number[dpc_name]
            alteration = Accidental(group_dict["comprehensive_accidental"]).semitones
            self._from_named_parts(dpc_number, alteration)
        elif isinstance(argument, numbers.Number):
            self._from_number(argument)
        elif isinstance(argument, (Pitch, PitchClass)):
            self._from_pitch_or_pitch_class(argument)
        else:
            try:
                pitch = NamedPitch(argument)
                self._from_pitch_or_pitch_class(pitch)
            except Exception:
                class_name = type(self).__name__
                message = f"can not instantiate {class_name} from {argument!r}."
                raise ValueError(message)

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
        Is true when pitch-class is less than ``argument``.

        Returns true or false.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _from_named_parts(self, dpc_number, alteration):
        raise NotImplementedError

    def _from_number(self, number):
        raise NotImplementedError

    def _from_pitch_or_pitch_class(self, pitch_or_pitch_class):
        raise NotImplementedError

    def _get_alteration(self):
        raise NotImplementedError

    def _get_diatonic_pc_number(self):
        raise NotImplementedError

    def _get_lilypond_format(self):
        raise NotImplementedError

    @staticmethod
    def _to_nearest_quarter_tone(number):
        number = round((float(number) % 12) * 4) / 4
        div, mod = divmod(number, 1)
        if mod == 0.75:
            div += 1
        elif mod == 0.5:
            div += 0.5
        div %= 12
        return math.integer_equivalent_number_to_integer(div)

    ### PUBLIC PROPERTIES ###

    def accidental(self):
        """
        Gets accidental of pitch-class.
        """
        raise NotImplementedError

    def pitch_class_label(self):
        """
        Gets pitch-class label of pitch-class.
        """
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def invert(self, axis=None):
        """
        Inverts pitch-class about ``axis``.

        Returns new pitch-class.
        """
        raise NotImplementedError

    def multiply(self, n=1):
        """
        Multiplies pitch-class by ``n``.

        Returns new pitch-class.
        """
        raise NotImplementedError

    def transpose(self, n=0):
        """
        Transposes pitch-class by index ``n``.

        Returns new pitch-class.
        """
        raise NotImplementedError


class NamedPitchClass(PitchClass):
    """
    Named pitch-class.

    ..  container:: example

        Initializes from pitch-class name:

        >>> abjad.NamedPitchClass('cs')
        NamedPitchClass('cs')

        >>> abjad.NamedPitchClass('cqs')
        NamedPitchClass('cqs')

    ..  container:: example

        Initializes from number of semitones:

        >>> abjad.NamedPitchClass(14)
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(14.5)
        NamedPitchClass('dqs')

    ..  container:: example

        Initializes from named pitch:

        >>> abjad.NamedPitchClass(abjad.NamedPitch('d'))
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(abjad.NamedPitch('dqs'))
        NamedPitchClass('dqs')

    ..  container:: example

        Initializes from numbered pitch:

        >>> abjad.NamedPitchClass(abjad.NumberedPitch(14))
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(abjad.NumberedPitch(14.5))
        NamedPitchClass('dqs')

    ..  container:: example

        Initializes from numbered pitch-class:

        >>> abjad.NamedPitchClass(abjad.NumberedPitchClass(2))
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(abjad.NumberedPitchClass(2.5))
        NamedPitchClass('dqs')

    ..  container:: example

        Initializes from pitch-class / octave-number string:

        >>> abjad.NamedPitchClass('C#5')
        NamedPitchClass('cs')

        >>> abjad.NamedPitchClass('Cs5')
        NamedPitchClass('cs')

        Initializes quartertone from pitch-class / octave-number string:

        >>> abjad.NamedPitchClass('C+5')
        NamedPitchClass('cqs')

        >>> abjad.NamedPitchClass('Cqs5')
        NamedPitchClass('cqs')

    ..  container:: example

        Initializes from pitch-class string:

        >>> abjad.NamedPitchClass('C#')
        NamedPitchClass('cs')

        >>> abjad.NamedPitchClass('Cs')
        NamedPitchClass('cs')

        >>> abjad.NamedPitchClass('cs')
        NamedPitchClass('cs')

        Initializes quartertone from pitch-class string

        >>> abjad.NamedPitchClass('C+')
        NamedPitchClass('cqs')

        >>> abjad.NamedPitchClass('Cqs')
        NamedPitchClass('cqs')

        >>> abjad.NamedPitchClass('cqs')
        NamedPitchClass('cqs')

    ..  container:: example

        Initializes from note:

        >>> abjad.NamedPitchClass(abjad.Note("d''8."))
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(abjad.Note("dqs''8."))
        NamedPitchClass('dqs')

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_diatonic_pc_number", "_accidental")

    ### INITIALIZER ###

    def __init__(self, name="c", *, accidental=None, arrow=None):
        super().__init__(name or "c")
        if accidental is not None:
            self._accidental = type(self._accidental)(accidental)
        if arrow is not None:
            self._accidental = type(self._accidental)(self._accidental, arrow=arrow)

    ### SPECIAL METHODS ###

    def __add__(self, named_interval):
        """
        Adds ``named_interval`` to named pitch-class.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs') + abjad.NamedInterval('+M9')
            NamedPitchClass('ds')

            >>> abjad.NamedPitchClass('cs') + abjad.NamedInterval('-M9')
            NamedPitchClass('b')

        Returns new named pitch-class.
        """
        dummy_pitch = NamedPitch((self.name, 4))
        pitch = named_interval.transpose(dummy_pitch)
        return type(self)(pitch)

    def __eq__(self, argument):
        """
        Is true when ``argument`` can be coerced to a named pitch-class with
        pitch-class name equal to that of this named pitch-class.

        ..  container:: example

            >>> pitch_class_1 = abjad.NamedPitchClass('cs')
            >>> pitch_class_2 = abjad.NamedPitchClass('cs')
            >>> pitch_class_3 = abjad.NamedPitchClass('df')

            >>> pitch_class_1 == pitch_class_1
            True
            >>> pitch_class_1 == pitch_class_2
            True
            >>> pitch_class_1 == pitch_class_3
            False

            >>> pitch_class_2 == pitch_class_1
            True
            >>> pitch_class_2 == pitch_class_2
            True
            >>> pitch_class_2 == pitch_class_3
            False

            >>> pitch_class_3 == pitch_class_1
            False
            >>> pitch_class_3 == pitch_class_2
            False
            >>> pitch_class_3 == pitch_class_3
            True

        Returns true or false.
        """
        return super().__eq__(argument)

    def __hash__(self):
        """
        Hashes named pitch-class.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super().__hash__()

    def __lt__(self, argument):
        """
        Is true when ``argument`` is a named pitch-class with a pitch
        number greater than that of this named pitch-class.

        ..  container:: example

            Compares less than:

            >>> abjad.NamedPitchClass('cs') < abjad.NamedPitchClass('d')
            True

        ..  container:: example

            Does not compare less than:

            >>> abjad.NamedPitchClass('d') < abjad.NamedPitchClass('cs')
            False

        Raises type error when ``argument`` is not a named pitch-class.
        """
        if not isinstance(argument, type(self)):
            raise TypeError(f"can not compare named pitch-class to {argument!r}.")
        return self.number < argument.number

    def __radd__(self, interval):
        """
        Right-addition not defined on named pitch-classes.

        ..  container:: example

            >>> abjad.NamedPitchClass("cs").__radd__(1)
            Traceback (most recent call last):
                ...
            NotImplementedError: right-addition not defined on NamedPitchClass.

        """
        message = f"right-addition not defined on {type(self).__name__}."
        raise NotImplementedError(message)

    def __str__(self):
        """
        Gets string representation of named pitch-class.

        ..  container:: example

            >>> str(abjad.NamedPitchClass('cs'))
            'cs'

        Returns string.
        """
        return self.name

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from named pitch-class.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs') - abjad.NamedPitchClass('g')
            NamedInversionEquivalentIntervalClass('+A4')

            >>> abjad.NamedPitchClass('c') - abjad.NamedPitchClass('cf')
            NamedInversionEquivalentIntervalClass('+A1')

            >>> abjad.NamedPitchClass('cf') - abjad.NamedPitchClass('c')
            NamedInversionEquivalentIntervalClass('+A1')

        Returns named inversion-equivalent interval-class.
        """
        from .intervalclasses import NamedInversionEquivalentIntervalClass
        from .intervals import NamedInterval

        if not isinstance(argument, type(self)):
            raise TypeError(f"must be named pitch-class: {argument!r}.")
        pitch_1 = NamedPitch((self.name, 4))
        pitch_2 = NamedPitch((argument.name, 4))
        mdi = NamedInterval.from_pitch_carriers(pitch_1, pitch_2)
        pair = (mdi.quality, mdi.number)
        dic = NamedInversionEquivalentIntervalClass(pair)
        return dic

    ### PRIVATE METHODS ###

    def _apply_accidental(self, accidental=None):
        accidental = Accidental(accidental)
        new_accidental = self.accidental + accidental
        new_name = self._get_diatonic_pc_name() + str(new_accidental)
        return type(self)(new_name)

    def _from_named_parts(self, dpc_number, alteration):
        self._diatonic_pc_number = dpc_number
        self._accidental = Accidental(alteration)

    def _from_number(self, number):
        numbered_pitch_class = NumberedPitchClass(number)
        self._from_pitch_or_pitch_class(numbered_pitch_class)

    def _from_pitch_or_pitch_class(self, pitch_or_pitch_class):
        if isinstance(pitch_or_pitch_class, Pitch):
            pitch_or_pitch_class = pitch_or_pitch_class.pitch_class
        self._diatonic_pc_number = pitch_or_pitch_class._get_diatonic_pc_number()
        self._accidental = Accidental(
            pitch_or_pitch_class._get_alteration(),
            arrow=pitch_or_pitch_class.arrow,
        )

    def _get_alteration(self):
        return self._accidental.semitones

    def _get_diatonic_pc_name(self):
        return _lib._diatonic_pc_number_to_diatonic_pc_name[self._diatonic_pc_number]

    def _get_diatonic_pc_number(self):
        return self._diatonic_pc_number

    def _get_format_specification(self):
        values = [self.name]
        return FormatSpecification(
            client=self,
            coerce_for_equality=True,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            storage_format_keyword_names=[],
        )

    def _get_lilypond_format(self):
        name = self._get_diatonic_pc_name()
        accidental = Accidental(self._get_alteration())
        return f"{name}{accidental!s}"

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        """
        Gets accidental.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs').accidental
            Accidental('sharp')

        Returns accidental.
        """
        return self._accidental

    @property
    def arrow(self):
        """
        Gets arrow of named pitch-class.

        Returns up, down or none.
        """
        return self._accidental.arrow

    @property
    def name(self):
        """
        Gets name of named pitch-class.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs').name
            'cs'

        Returns string.
        """
        diatonic_pc_name = _lib._diatonic_pc_number_to_diatonic_pc_name[
            self._diatonic_pc_number
        ]
        return f"{diatonic_pc_name}{self._accidental!s}"

    @property
    def number(self):
        """
        Gets number.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs').number
            1

        Returns nonnegative integer or float.
        """
        dictionary = _lib._diatonic_pc_number_to_pitch_class_number
        result = dictionary[self._diatonic_pc_number]
        result += self._accidental.semitones
        result %= 12
        return result

    @property
    def pitch_class_label(self):
        """
        Gets pitch-class label.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs').pitch_class_label
            'C#'

        Returns string.
        """
        pc = self._get_diatonic_pc_name().upper()
        return f"{pc}{self.accidental.symbol}"

    ### PUBLIC METHODS ###

    def invert(self, axis=None):
        """
        Inverts named pitch-class.

        Not yet implemented.
        """
        axis = axis or NamedPitch("c")
        axis = NamedPitch(axis)
        this = NamedPitch(self)
        interval = this - axis
        result = axis.transpose(interval)
        result = type(self)(result)
        return result

    def multiply(self, n=1):
        """
        Multiplies named pitch-class by ``n``.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs').multiply(3)
            NamedPitchClass('ef')

        Returns new named pitch-class.
        """
        return type(self)(n * self.number)

    def transpose(self, n=0):
        """
        Transposes named pitch-class by index named interval ``n``.

        ..  container:: example

            >>> interval = abjad.NamedInterval('-M2')
            >>> abjad.NamedPitchClass('cs').transpose(interval)
            NamedPitchClass('b')

            >>> interval = abjad.NamedInterval('P1')
            >>> abjad.NamedPitchClass('cs').transpose(interval)
            NamedPitchClass('cs')

            >>> interval = abjad.NamedInterval('+M2')
            >>> abjad.NamedPitchClass('cs').transpose(interval)
            NamedPitchClass('ds')

        Returns new named pitch-class.
        """
        from .intervals import NamedInterval

        interval = NamedInterval(n)
        pitch = NamedPitch((self.name, 4))
        pitch = interval.transpose(pitch)
        return type(self)(pitch)


class NumberedPitchClass(PitchClass):
    """
    Numbered pitch-class.

    ..  container:: example

        Initializes from number of semitones:

        >>> abjad.NumberedPitchClass(13)
        NumberedPitchClass(1)

    ..  container:: example

        Initializes from pitch name.

        >>> abjad.NumberedPitchClass('d')
        NumberedPitchClass(2)

    ..  container:: example

        Initializes from named pitch.

        >>> abjad.NumberedPitchClass(abjad.NamedPitch('g,'))
        NumberedPitchClass(7)

    ..  container:: example

        Initializes from numbered pitch.

        >>> abjad.NumberedPitchClass(abjad.NumberedPitch(15))
        NumberedPitchClass(3)

    ..  container:: example

        Initializes from named pitch-class.

        >>> abjad.NumberedPitchClass(abjad.NamedPitchClass('e'))
        NumberedPitchClass(4)

    ..  container:: example

        Initializes from pitch-class / octave string:

        >>> abjad.NumberedPitchClass('C#5')
        NumberedPitchClass(1)

    ..  container:: example

        Initializes from other numbered pitch-class:

        >>> abjad.NumberedPitchClass(abjad.NumberedPitchClass(9))
        NumberedPitchClass(9)

    ..  container:: example

        Initializes from note:

        >>> abjad.NumberedPitchClass(abjad.Note("a'8."))
        NumberedPitchClass(9)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_arrow", "_number")

    ### INITIALIZER ###

    def __init__(self, number=0, *, arrow=None):
        super().__init__(number or 0)
        if arrow is not None:
            arrow = enums.VerticalAlignment.from_expr(arrow)
            if arrow is enums.Center:
                arrow = None
            self._arrow = arrow

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        """
        Adds ``argument`` to numbered pitch-class.

        ..  container:: example

            >>> pitch_class = abjad.NumberedPitchClass(9)

            >>> pitch_class + abjad.NumberedInterval(0)
            NumberedPitchClass(9)

            >>> pitch_class + abjad.NumberedInterval(1)
            NumberedPitchClass(10)

            >>> pitch_class + abjad.NumberedInterval(2)
            NumberedPitchClass(11)

            >>> pitch_class + abjad.NumberedInterval(3)
            NumberedPitchClass(0)

        Returns new numbered pitch-class.
        """
        from .intervals import NumberedInterval

        interval = NumberedInterval(argument)
        return type(self)(self.number + interval.number % 12)

    def __copy__(self, *arguments):
        """
        Copies numbered pitch-class.

        ..  container:: example

            >>> import copy
            >>> pitch_class = abjad.NumberedPitchClass(9)
            >>> copy.copy(pitch_class)
            NumberedPitchClass(9)

        Returns new numbered pitch-class.
        """
        return type(self)(self)

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a numbered pitch-class with pitch-class
        number equal to that of this numbered pitch-class.

        ..  container:: example

            >>> pitch_class_1 = abjad.NumberedPitchClass(0)
            >>> pitch_class_2 = abjad.NumberedPitchClass(0)
            >>> pitch_class_3 = abjad.NumberedPitchClass(1)

            >>> pitch_class_1 == pitch_class_1
            True
            >>> pitch_class_1 == pitch_class_2
            True
            >>> pitch_class_1 == pitch_class_3
            False

            >>> pitch_class_2 == pitch_class_1
            True
            >>> pitch_class_2 == pitch_class_2
            True
            >>> pitch_class_2 == pitch_class_3
            False

            >>> pitch_class_3 == pitch_class_1
            False
            >>> pitch_class_3 == pitch_class_2
            False
            >>> pitch_class_3 == pitch_class_3
            True

        Returns true or false.
        """
        return super().__eq__(argument)

    def __hash__(self):
        """
        Hashes numbered pitch-class.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super().__hash__()

    def __lt__(self, argument):
        """
        Is true when ``argument`` is a numbered pitch-class with a pitch
        number greater than that of this numberd pitch-class.

        ..  container:: example

            Compares less than:

            >>> abjad.NumberedPitchClass(1) < abjad.NumberedPitchClass(2)
            True

        ..  container:: example

            Does not compare less than:

            >>> abjad.NumberedPitchClass(2) < abjad.NumberedPitchClass(1)
            False

        Raises type error when ``argument`` is not a numbered pitch-class.
        """
        if not isinstance(argument, type(self)):
            raise TypeError(f"can not compare numbered pitch-class to {argument!r}.")
        return self.number < argument.number

    def __neg__(self):
        """
        Negates numbered pitch-class.

        ..  container:: example

            >>> pitch_class = abjad.NumberedPitchClass(9)
            >>> -pitch_class
            NumberedPitchClass(3)

        Returns new numbered pitch-class.
        """
        return type(self)(-self.number)

    def __radd__(self, argument):
        """
        Right-addition not defined on numbered pitch-classes.

        ..  container:: example

            >>> 1 + abjad.NumberedPitchClass(9)
            Traceback (most recent call last):
                ...
            NotImplementedError: right-addition not defined on NumberedPitchClass.

        Raises not implemented error.
        """
        message = f"right-addition not defined on {type(self).__name__}."
        raise NotImplementedError(message)

    def __str__(self):
        """
        Gets string representation of numbered pitch-class.

        Returns string.
        """
        return str(self.number)

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from numbered pitch-class.

        Subtraction is defined against both numbered intervals
        and against other pitch-classes.

        ..  container:: example

            >>> abjad.NumberedPitchClass(6) - abjad.NumberedPitchClass(6)
            NumberedInversionEquivalentIntervalClass(0)

            >>> abjad.NumberedPitchClass(6) - abjad.NumberedPitchClass(7)
            NumberedInversionEquivalentIntervalClass(1)

            >>> abjad.NumberedPitchClass(7) - abjad.NumberedPitchClass(6)
            NumberedInversionEquivalentIntervalClass(1)

        ..  container:: example

            >>> abjad.NumberedPitchClass(6) - abjad.NumberedInterval(-1)
            NumberedPitchClass(5)

            >>> abjad.NumberedPitchClass(6) - abjad.NumberedInterval(0)
            NumberedPitchClass(6)

            >>> abjad.NumberedPitchClass(6) - abjad.NumberedInterval(1)
            NumberedPitchClass(5)

        Returns numbered inversion-equivalent interval-class.
        """
        from .intervalclasses import NumberedInversionEquivalentIntervalClass

        if isinstance(argument, type(self)):
            interval_class_number = abs(self.number - argument.number)
            if 6 < interval_class_number:
                interval_class_number = 12 - interval_class_number
            return NumberedInversionEquivalentIntervalClass(interval_class_number)
        interval_class = NumberedInversionEquivalentIntervalClass(argument)
        return type(self)(self.number - interval_class.number % 12)

    ### PRIVATE METHODS ###

    def _apply_accidental(self, accidental=None):
        accidental = Accidental(accidental)
        semitones = self.number + accidental.semitones
        return type(self)(semitones)

    def _from_named_parts(self, dpc_number, alteration):
        number = _lib._diatonic_pc_number_to_pitch_class_number[dpc_number]
        number += alteration
        self._from_number(number)

    def _from_number(self, number):
        self._arrow = None
        self._number = self._to_nearest_quarter_tone(number)

    def _from_pitch_or_pitch_class(self, pitch_or_pitch_class):
        self._arrow = pitch_or_pitch_class.arrow
        self._number = self._to_nearest_quarter_tone(float(pitch_or_pitch_class))

    def _get_alteration(self):
        dpc_number = self._get_diatonic_pc_number()
        pc_number = _lib._diatonic_pc_number_to_pitch_class_number[dpc_number]
        return float(self) - pc_number

    def _get_diatonic_pc_name(self):
        return self.name[0]

    def _get_diatonic_pc_number(self):
        return _lib._diatonic_pc_name_to_diatonic_pc_number[
            self._get_diatonic_pc_name()
        ]

    def _get_format_specification(self):
        values = [self.number]
        return FormatSpecification(
            client=self,
            coerce_for_equality=True,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            storage_format_keyword_names=[],
        )

    def _get_lilypond_format(self):
        return NamedPitchClass(self)._get_lilypond_format()

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        """
        Gets accidental.

        ..  container:: example

            >>> abjad.NumberedPitchClass(1).accidental
            Accidental('sharp')

        Returns accidental.
        """
        return NamedPitch(self.number).accidental

    @property
    def arrow(self):
        """
        Gets arrow of numbered pitch-class.

        Returns up, down or none.
        """
        return self._arrow

    @property
    def name(self):
        """
        Gets name of numbered pitch-class.

        ..  container:: example

            >>> abjad.NumberedPitchClass(13).name
            'cs'

        Returns string.
        """
        return _lib._pitch_class_number_to_pitch_class_name[self.number]

    @property
    def number(self):
        """
        Gets number.

        ..  container:: example

            >>> abjad.NumberedPitchClass(1).number
            1

        ..  container:: example

            >>> abjad.NumberedPitchClass(13).number
            1

        """
        return self._number

    @property
    def pitch_class_label(self):
        """
        Gets pitch-class / octave label.

        ..  container:: example

            >>> abjad.NumberedPitchClass(13).pitch_class_label
            'C#'

        Returns string.
        """
        name = self._get_diatonic_pc_name().upper()
        return f"{name}{self.accidental.symbol}"

    ### PUBLIC METHODS ###

    def invert(self, axis=None):
        """
        Inverts numbered pitch-class.

        ..  container:: example

            >>> for n in range(12):
            ...     pitch_class = abjad.NumberedPitchClass(n)
            ...     print(repr(pitch_class), repr(pitch_class.invert()))
            ...
            NumberedPitchClass(0) NumberedPitchClass(0)
            NumberedPitchClass(1) NumberedPitchClass(11)
            NumberedPitchClass(2) NumberedPitchClass(10)
            NumberedPitchClass(3) NumberedPitchClass(9)
            NumberedPitchClass(4) NumberedPitchClass(8)
            NumberedPitchClass(5) NumberedPitchClass(7)
            NumberedPitchClass(6) NumberedPitchClass(6)
            NumberedPitchClass(7) NumberedPitchClass(5)
            NumberedPitchClass(8) NumberedPitchClass(4)
            NumberedPitchClass(9) NumberedPitchClass(3)
            NumberedPitchClass(10) NumberedPitchClass(2)
            NumberedPitchClass(11) NumberedPitchClass(1)

        Interprets axis of inversion equal to pitch-class 0.

        Returns new numbered pitch-class.
        """
        axis = axis or NumberedPitch("c")
        axis = NumberedPitch(axis)
        this = NumberedPitch(self)
        interval = this - axis
        result = axis.transpose(interval)
        result = type(self)(result)
        return result

    def multiply(self, n=1):
        """
        Multiplies pitch-class number by ``n``.

        ..  container:: example

            >>> for n in range(12):
            ...     pitch_class = abjad.NumberedPitchClass(n)
            ...     print(repr(pitch_class), repr(pitch_class.multiply(5)))
            ...
            NumberedPitchClass(0) NumberedPitchClass(0)
            NumberedPitchClass(1) NumberedPitchClass(5)
            NumberedPitchClass(2) NumberedPitchClass(10)
            NumberedPitchClass(3) NumberedPitchClass(3)
            NumberedPitchClass(4) NumberedPitchClass(8)
            NumberedPitchClass(5) NumberedPitchClass(1)
            NumberedPitchClass(6) NumberedPitchClass(6)
            NumberedPitchClass(7) NumberedPitchClass(11)
            NumberedPitchClass(8) NumberedPitchClass(4)
            NumberedPitchClass(9) NumberedPitchClass(9)
            NumberedPitchClass(10) NumberedPitchClass(2)
            NumberedPitchClass(11) NumberedPitchClass(7)

        Returns new numbered pitch-class.
        """
        return type(self)(n * self.number)

    def transpose(self, n=0):
        """
        Transposes numbered pitch-class by index ``n``.

        ..  container:: example

            >>> for n in range(12):
            ...     pitch_class = abjad.NumberedPitchClass(n)
            ...     print(repr(pitch_class), repr(pitch_class.transpose(-13)))
            ...
            NumberedPitchClass(0) NumberedPitchClass(11)
            NumberedPitchClass(1) NumberedPitchClass(0)
            NumberedPitchClass(2) NumberedPitchClass(1)
            NumberedPitchClass(3) NumberedPitchClass(2)
            NumberedPitchClass(4) NumberedPitchClass(3)
            NumberedPitchClass(5) NumberedPitchClass(4)
            NumberedPitchClass(6) NumberedPitchClass(5)
            NumberedPitchClass(7) NumberedPitchClass(6)
            NumberedPitchClass(8) NumberedPitchClass(7)
            NumberedPitchClass(9) NumberedPitchClass(8)
            NumberedPitchClass(10) NumberedPitchClass(9)
            NumberedPitchClass(11) NumberedPitchClass(10)

        Returns new numbered pitch-class.
        """
        return type(self)(self.number + n)
