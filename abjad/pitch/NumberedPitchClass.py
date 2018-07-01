from abjad import enums
from abjad.system.FormatSpecification import FormatSpecification
from . import constants
from .PitchClass import PitchClass


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

    __slots__ = (
        '_arrow',
        '_number',
        )

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
        Adds `argument` to numbered pitch-class.

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
        import abjad
        interval = abjad.NumberedInterval(argument)
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
        Is true when `argument` is a numbered pitch-class with pitch-class
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

    def __format__(self, format_specification=''):
        """
        Formats numbered pitch-class.

        ..  container:: example

            >>> format(abjad.NumberedPitchClass(13))
            'abjad.NumberedPitchClass(1)'

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.

        Returns string.
        """
        return super().__format__(format_specification=format_specification)

    def __hash__(self):
        """
        Hashes numbered pitch-class.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super().__hash__()

    def __lt__(self, argument):
        """
        Is true when `argument` is a numbered pitch-class with a pitch
        number greater than that of this numberd pitch-class.

        ..  container:: example

            Compares less than:

            >>> abjad.NumberedPitchClass(1) < abjad.NumberedPitchClass(2)
            True

        ..  container:: example

            Does not compare less than:

            >>> abjad.NumberedPitchClass(2) < abjad.NumberedPitchClass(1)
            False

        Raises type error when `argument` is not a numbered pitch-class.
        """
        if not isinstance(argument, type(self)):
            message = 'can not compare numbered pitch-class to {!r}.'
            message = message.format(argument)
            raise TypeError(message)
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
        message = 'right-addition not defined on {}.'
        message = message.format(type(self).__name__)
        raise NotImplementedError(message)

    def __str__(self):
        """
        Gets string representation of numbered pitch-class.

        Returns string.
        """
        return str(self.number)

    def __sub__(self, argument):
        """
        Subtracts `argument` from numbered pitch-class.

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
        import abjad
        if isinstance(argument, type(self)):
            interval_class_number = abs(
                self.number - argument.number
                )
            if 6 < interval_class_number:
                interval_class_number = 12 - interval_class_number
            return abjad.NumberedInversionEquivalentIntervalClass(
                interval_class_number)
        interval_class = abjad.NumberedInversionEquivalentIntervalClass(
            argument)
        return type(self)(self.number - interval_class.number % 12)

    ### PRIVATE METHODS ###

    def _apply_accidental(self, accidental=None):
        import abjad
        accidental = abjad.Accidental(accidental)
        semitones = self.number + accidental.semitones
        return type(self)(semitones)

    def _from_named_parts(self, dpc_number, alteration):
        number = constants._diatonic_pc_number_to_pitch_class_number[dpc_number]
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
        pc_number = constants._diatonic_pc_number_to_pitch_class_number[dpc_number]
        return float(self) - pc_number

    def _get_diatonic_pc_name(self):
        return self.name[0]

    def _get_diatonic_pc_number(self):
        return constants._diatonic_pc_name_to_diatonic_pc_number[
            self._get_diatonic_pc_name()]

    def _get_format_specification(self):
        values = [self.number]
        return FormatSpecification(
            client=self,
            coerce_for_equality=True,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            storage_format_kwargs_names=[],
            )

    def _get_lilypond_format(self):
        import abjad
        return format(abjad.NamedPitchClass(self), 'lilypond')

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
        import abjad
        return abjad.NamedPitch(self.number).accidental

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
        return constants._pitch_class_number_to_pitch_class_name[self.number]

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
        return '{}{}'.format(
            self._get_diatonic_pc_name().upper(),
            self.accidental.symbol,
            )

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
        import abjad
        axis = axis or abjad.NumberedPitch('c')
        axis = abjad.NumberedPitch(axis)
        this = abjad.NumberedPitch(self)
        interval = this - axis
        result = axis.transpose(interval)
        result = type(self)(result)
        return result

    def multiply(self, n=1):
        """
        Multiplies pitch-class number by `n`.

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
        Transposes numbered pitch-class by index `n`.

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
