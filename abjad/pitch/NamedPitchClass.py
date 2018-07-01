from abjad.system.FormatSpecification import FormatSpecification
from . import constants
from .Pitch import Pitch
from .PitchClass import PitchClass


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

    __slots__ = (
        '_diatonic_pc_number',
        '_accidental',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name='c',
        *,
        accidental=None,
        arrow=None,
    ):
        super().__init__(name or 'c')
        if accidental is not None:
            self._accidental = type(self._accidental)(accidental)
        if arrow is not None:
            self._accidental = type(self._accidental)(
                self._accidental,
                arrow=arrow,
                )

    ### SPECIAL METHODS ###

    def __add__(self, named_interval):
        """
        Adds `named_interval` to named pitch-class.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs') + abjad.NamedInterval('+M9')
            NamedPitchClass('ds')

            >>> abjad.NamedPitchClass('cs') + abjad.NamedInterval('-M9')
            NamedPitchClass('b')

        Returns new named pitch-class.
        """
        import abjad
        dummy_pitch = abjad.NamedPitch((self.name, 4))
        pitch = named_interval.transpose(dummy_pitch)
        return type(self)(pitch)

    def __copy__(self, *arguments):
        """
        Copies named pitch-class.

        ..  container:: example

            >>> import copy
            >>> copy.copy(abjad.NamedPitchClass('cs'))
            NamedPitchClass('cs')

        Returns new named pitch-class.
        """
        return super().__copy__(*arguments)

    def __eq__(self, argument):
        """
        Is true when `argument` can be coerced to a named pitch-class with
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

    def __format__(self, format_specification=''):
        """
        Formats named pitch-class.

        ..  container:: example

            >>> format(abjad.NamedPitchClass('cs'))
            "abjad.NamedPitchClass('cs')"

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.

        Returns string.
        """
        return super().__format__(format_specification=format_specification)

    def __hash__(self):
        """
        Hashes named pitch-class.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super().__hash__()

    def __lt__(self, argument):
        """
        Is true when `argument` is a named pitch-class with a pitch
        number greater than that of this named pitch-class.

        ..  container:: example

            Compares less than:

            >>> abjad.NamedPitchClass('cs') < abjad.NamedPitchClass('d')
            True

        ..  container:: example

            Does not compare less than:

            >>> abjad.NamedPitchClass('d') < abjad.NamedPitchClass('cs')
            False

        Raises type error when `argument` is not a named pitch-class.
        """
        if not isinstance(argument, type(self)):
            message = 'can not compare named pitch-class to {!r}.'
            message = message.format(argument)
            raise TypeError(message)
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
        message = 'right-addition not defined on {}.'
        message = message.format(type(self).__name__)
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
        Subtracts `argument` from named pitch-class.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs') - abjad.NamedPitchClass('g')
            NamedInversionEquivalentIntervalClass('+A4')

            >>> abjad.NamedPitchClass('c') - abjad.NamedPitchClass('cf')
            NamedInversionEquivalentIntervalClass('+A1')

            >>> abjad.NamedPitchClass('cf') - abjad.NamedPitchClass('c')
            NamedInversionEquivalentIntervalClass('+A1')

        Returns named inversion-equivalent interval-class.
        """
        import abjad
        if not isinstance(argument, type(self)):
            message = 'must be named pitch-class: {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        pitch_1 = abjad.NamedPitch((self.name, 4))
        pitch_2 = abjad.NamedPitch((argument.name, 4))
        mdi = abjad.NamedInterval.from_pitch_carriers(pitch_1, pitch_2)
        pair = (mdi.quality, mdi.number)
        dic = abjad.NamedInversionEquivalentIntervalClass(pair)
        return dic

    ### PRIVATE METHODS ###

    def _apply_accidental(self, accidental=None):
        import abjad
        accidental = abjad.Accidental(accidental)
        new_accidental = self.accidental + accidental
        new_name = self._get_diatonic_pc_name() + str(new_accidental)
        return type(self)(new_name)

    def _from_named_parts(self, dpc_number, alteration):
        import abjad
        self._diatonic_pc_number = dpc_number
        self._accidental = abjad.Accidental(alteration)

    def _from_number(self, number):
        import abjad
        numbered_pitch_class = abjad.NumberedPitchClass(number)
        self._from_pitch_or_pitch_class(numbered_pitch_class)

    def _from_pitch_or_pitch_class(self, pitch_or_pitch_class):
        import abjad
        if isinstance(pitch_or_pitch_class, Pitch):
            pitch_or_pitch_class = pitch_or_pitch_class.pitch_class
        self._diatonic_pc_number = pitch_or_pitch_class._get_diatonic_pc_number()
        self._accidental = abjad.Accidental(
            pitch_or_pitch_class._get_alteration(),
            arrow=pitch_or_pitch_class.arrow,
            )

    def _get_alteration(self):
        return self._accidental.semitones

    def _get_diatonic_pc_number(self):
        return self._diatonic_pc_number

    def _get_diatonic_pc_name(self):
        return constants._diatonic_pc_number_to_diatonic_pc_name[
            self._diatonic_pc_number]

    def _get_format_specification(self):
        values = [self.name]
        return FormatSpecification(
            client=self,
            coerce_for_equality=True,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            storage_format_kwargs_names=[],
            )

    def _get_lilypond_format(self):
        import abjad
        return '{}{!s}'.format(
            self._get_diatonic_pc_name(),
            abjad.Accidental(self._get_alteration()),
            )

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
        diatonic_pc_name = constants._diatonic_pc_number_to_diatonic_pc_name[
            self._diatonic_pc_number
            ]
        return '{}{!s}'.format(diatonic_pc_name, self._accidental)

    @property
    def number(self):
        """
        Gets number.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs').number
            1

        Returns nonnegative integer or float.
        """
        dictionary = constants._diatonic_pc_number_to_pitch_class_number
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
        return '{}{}'.format(
            self._get_diatonic_pc_name().upper(),
            self.accidental.symbol,
            )

    ### PUBLIC METHODS ###

    def invert(self, axis=None):
        """
        Inverts named pitch-class.

        Not yet implemented.
        """
        import abjad
        axis = axis or abjad.NamedPitch('c')
        axis = abjad.NamedPitch(axis)
        this = abjad.NamedPitch(self)
        interval = this - axis
        result = axis.transpose(interval)
        result = type(self)(result)
        return result

    def multiply(self, n=1):
        """
        Multiplies named pitch-class by `n`.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs').multiply(3)
            NamedPitchClass('ef')

        Returns new named pitch-class.
        """
        return type(self)(n * self.number)

    def transpose(self, n=0):
        """
        Transposes named pitch-class by index named interval `n`.

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
        import abjad
        interval = abjad.NamedInterval(n)
        pitch = abjad.NamedPitch((self.name, 4))
        pitch = interval.transpose(pitch)
        return type(self)(pitch)
