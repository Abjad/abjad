import numbers
from abjad.tools import mathtools
from abjad.tools.pitchtools.PitchClass import PitchClass


class NumberedPitchClass(PitchClass):
    '''Numbered pitch-class.

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

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    ### INITIALIZER ###

    def __init__(self, number=0):
        from abjad.tools import pitchtools
        prototype = (numbers.Number, pitchtools.NumberedPitch, type(self))
        if isinstance(number, numbers.Number):
            self._initialize_by_number(float(number))
        elif isinstance(number, prototype):
            self._initialize_by_number(float(number.number))
        elif isinstance(number, pitchtools.NamedPitch):
            self._initialize_by_named_pitch(number)
        elif isinstance(number, pitchtools.NamedPitchClass):
            self._initialize_by_named_pitch_class(number)
        elif isinstance(number, str):
            self._initialize_by_string(number)
        elif pitchtools.Pitch._is_pitch_carrier(number):
            self._initialize_by_pitch_carrier(number)
        else:
            message = 'can not instantiate {} from {!r}.'
            message = message.format(type(self).__name__, number)
            raise TypeError(message)

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        r'''Adds `argument` to numbered pitch-class.

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
        '''
        from abjad.tools import pitchtools
        interval = pitchtools.NumberedInterval(argument)
        return type(self)(self.number + interval.number % 12)

    def __copy__(self, *arguments):
        r'''Copies numbered pitch-class.

        ..  container:: example

            >>> import copy
            >>> pitch_class = abjad.NumberedPitchClass(9)
            >>> copy.copy(pitch_class)
            NumberedPitchClass(9)

        Returns new numbered pitch-class.
        '''
        return type(self)(self)

    def __eq__(self, argument):
        r'''Is true when `argument` is a numbered pitch-class with pitch-class
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
        '''
        return super(NumberedPitchClass, self).__eq__(argument)

    def __format__(self, format_specification=''):
        r'''Formats numbered pitch-class.

        ..  container:: example

            >>> format(abjad.NumberedPitchClass(13))
            'abjad.NumberedPitchClass(1)'

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.

        Returns string.
        '''
        superclass = super(NumberedPitchClass, self)
        return superclass.__format__(format_specification=format_specification)

    def __hash__(self):
        r'''Hashes numbered pitch-class.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(NumberedPitchClass, self).__hash__()

    def __lt__(self, argument):
        r'''Is true when `argument` is a numbered pitch-class with a pitch
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
        '''
        if not isinstance(argument, type(self)):
            message = 'can not compare numbered pitch-class to {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        return self.number < argument.number

    def __neg__(self):
        r'''Negates numbered pitch-class.

        ..  container:: example

            >>> pitch_class = abjad.NumberedPitchClass(9)
            >>> -pitch_class
            NumberedPitchClass(3)

        Returns new numbered pitch-class.
        '''
        return type(self)(-self.number)

    def __radd__(self, argument):
        r'''Right-addition not defined on numbered pitch-classes.

        ..  container:: example

            >>> 1 + abjad.NumberedPitchClass(9)
            Traceback (most recent call last):
            ...
            NotImplementedError: right-addition not defined on NumberedPitchClass.

        Raises not implemented error.
        '''
        message = 'right-addition not defined on {}.'
        message = message.format(type(self).__name__)
        raise NotImplementedError(message)

    def __str__(self):
        r'''Gets string representation of numbered pitch-class.

        Returns string.
        '''
        return str(self.number)

    def __sub__(self, argument):
        r'''Subtracts `argument` from numbered pitch-class.

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
        '''
        from abjad.tools import pitchtools
        if isinstance(argument, type(self)):
            interval_class_number = abs(
                self.number - argument.number
                )
            if 6 < interval_class_number:
                interval_class_number = 12 - interval_class_number
            return pitchtools.NumberedInversionEquivalentIntervalClass(
                interval_class_number)
        interval_class = pitchtools.NumberedInversionEquivalentIntervalClass(
            argument)
        return type(self)(self.number - interval_class.number % 12)

    ### PRIVATE METHODS ###

    def _apply_accidental(self, accidental=None):
        from abjad.tools import pitchtools
        accidental = pitchtools.Accidental(accidental)
        semitones = self.number + accidental.semitones
        return type(self)(semitones)

    def _get_diatonic_pitch_class_name(self):
        return self.name[0]

    def _get_diatonic_pitch_class_number(self):
        return self._diatonic_pitch_class_name_to_diatonic_pitch_class_number[
            self._get_diatonic_pitch_class_name()]

    def _get_format_specification(self):
        import abjad
        values = [self.number]
        return abjad.FormatSpecification(
            client=self,
            coerce_for_equality=True,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            )

    def _initialize_by_named_pitch(self, argument):
        self._number = argument.pitch_class.number

    def _initialize_by_named_pitch_class(self, argument):
        self._number = argument.number

    def _initialize_by_number(self, argument):
        argument = round((float(argument) % 12) * 4) / 4
        div, mod = divmod(argument, 1)
        if mod == 0.75:
            div += 1
        elif mod == 0.5:
            div += 0.5
        div %= 12
        self._number = mathtools.integer_equivalent_number_to_integer(div)

    def _initialize_by_pitch_carrier(self, argument):
        from abjad.tools import pitchtools
        named_pitch = pitchtools.NamedPitch.from_pitch_carrier(argument)
        self._initialize_by_named_pitch(named_pitch)

    def _initialize_by_string(self, argument):
        from abjad.tools import pitchtools
        named_pitch_class = pitchtools.NamedPitchClass(argument)
        self._initialize_by_named_pitch_class(named_pitch_class)

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        r'''Gets accidental.

        ..  container:: example

            >>> abjad.NumberedPitchClass(1).accidental
            Accidental('sharp')

        Returns accidental.
        '''
        import abjad
        return abjad.NamedPitch(self.number).accidental

    @property
    def name(self):
        r'''Gets name of numbered pitch-class.

        ..  container:: example

            >>> abjad.NumberedPitchClass(13).name
            'cs'

        Returns string.
        '''
        from abjad import abjad_configuration
        accidental_spelling = abjad_configuration['accidental_spelling']
        if accidental_spelling == 'mixed':
            return self._pitch_class_number_to_pitch_class_name[self.number]
        elif accidental_spelling == 'sharps':
            return self._pitch_class_number_to_pitch_class_name_with_sharps[
                self.number]
        elif accidental_spelling == 'flats':
            return self._pitch_class_number_to_pitch_class_name_with_flats[
                self.number]
        else:
            message = 'unknown accidental spelling: {!r}.'
            message = message.format(accidental_spelling)
            raise ValueError(message)

    @property
    def number(self):
        r'''Gets number.

        ..  container:: example

            >>> abjad.NumberedPitchClass(1).number
            1

        ..  container:: example

            >>> abjad.NumberedPitchClass(13).number
            1

        '''
        return self._number

    @property
    def pitch_class_label(self):
        r'''Gets pitch-class / octave label.

        ..  container:: example

            >>> abjad.NumberedPitchClass(13).pitch_class_label
            'C#'

        Returns string.
        '''
        return '{}{}'.format(
            self._get_diatonic_pitch_class_name().upper(),
            self.accidental.symbol,
            )

    ### PUBLIC METHODS ###

    def invert(self, axis=None):
        r'''Inverts numbered pitch-class.

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
        '''
        from abjad.tools import pitchtools
        axis = axis or pitchtools.NumberedPitch('c')
        axis = pitchtools.NumberedPitch(axis)
        this = pitchtools.NumberedPitch(self)
        interval = this - axis
        result = axis.transpose(interval)
        result = type(self)(result)
        return result

    def multiply(self, n=1):
        r'''Multiplies pitch-class number by `n`.

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
        '''
        return type(self)(n * self.number)

    def transpose(self, n=0):
        r'''Transposes numbered pitch-class by index `n`.

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
        '''
        return type(self)(self.number + n)
