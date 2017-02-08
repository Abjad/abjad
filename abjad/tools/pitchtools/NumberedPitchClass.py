# -*- coding: utf-8 -*-
import functools
import numbers
from abjad.tools import mathtools
from abjad.tools.pitchtools.PitchClass import PitchClass


@functools.total_ordering
class NumberedPitchClass(PitchClass):
    '''Numbered pitch-class.

    ..  container:: example

        Initializes from number of semitones:

        ::

            >>> NumberedPitchClass(13)
            NumberedPitchClass(1)

    ..  container:: example

        Initializes from pitch name.

        ::

            >>> NumberedPitchClass('d')
            NumberedPitchClass(2)

    ..  container:: example

        Initializes from named pitch.

        ::

            >>> NumberedPitchClass(NamedPitch('g,'))
            NumberedPitchClass(7)

    ..  container:: example

        Initializes from numbered pitch.

        ::

            >>> NumberedPitchClass(NumberedPitch(15))
            NumberedPitchClass(3)

    ..  container:: example

        Initializes from named pitch-class.

        ::

            >>> NumberedPitchClass(NamedPitchClass('e'))
            NumberedPitchClass(4)

    ..  container:: example

        Initializes from numbered pitch-class.

        ::

            >>> NumberedPitchClass('C#5')
            NumberedPitchClass(1)

    ..  container:: example

        Initializes from numbered pitch-class.

        ::

            >>> NumberedPitchClass(Note("a'8."))
            NumberedPitchClass(9)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pitch_class_number',
        )

    ### INITIALIZER ###

    def __init__(self, argument=None):
        from abjad.tools import pitchtools
        prototype = (numbers.Number, pitchtools.NumberedPitch, type(self))
        if isinstance(argument, prototype):
            self._initialize_by_number(float(argument))
        elif isinstance(argument, pitchtools.NamedPitch):
            self._initialize_by_named_pitch(argument)
        elif isinstance(argument, pitchtools.NamedPitchClass):
            self._initialize_by_named_pitch_class(argument)
        elif isinstance(argument, str):
            self._initialize_by_string(argument)
        elif pitchtools.Pitch.is_pitch_carrier(argument):
            self._initialize_by_pitch_carrier(argument)
        elif argument is None:
            self._initialize_by_number(0)
        else:
            message = 'can not instantiate {} from {!r}.'
            message = message.format(type(self).__name__, argument)
            raise TypeError(message)

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        r'''Adds `argument` to numbered pitch-class.

        ..  container:: example

            ::

                >>> pitch_class = NumberedPitchClass(9)
                >>> interval = NumberedInterval(4)
                >>> pitch_class + interval
                NumberedPitchClass(1)

        Returns new numbered pitch-class.
        '''
        from abjad.tools import pitchtools
        interval = pitchtools.NumberedInterval(argument)
        return type(self)(self.pitch_class_number + interval.number % 12)

    def __copy__(self, *arguments):
        r'''Copies numbered pitch-class.

        ..  container:: example

            ::

                >>> import copy
                >>> pitch_class = NumberedPitchClass(9)
                >>> copy.copy(pitch_class)
                NumberedPitchClass(9)

        Returns new numbered pitch-class.
        '''
        return type(self)(self)

    def __eq__(self, argument):
        r'''Is true when `argument` is a numbered pitch-class with pitch-class
        number equal to that of this numbered pitch-class.

        ..  container:: example

            ::

                >>> pitch_class_1 = NumberedPitchClass(9)
                >>> pitch_class_2 = NumberedPitchClass(3)
                >>> pitch_class_1 == pitch_class_1
                True

        Otherwise false:

        ..  container:: example

            ::

                >>> pitch_class_1 == pitch_class_2
                False

        Returns true or false.
        '''
        if isinstance(argument, type(self)):
            return self._pitch_class_number == \
                argument._pitch_class_number
        return self._pitch_class_number == argument

    def __float__(self):
        r'''Changes numbered pitch-class to float.

        ..  container:: example

            ::

                >>> pitch_class = NumberedPitchClass(9)
                >>> float(pitch_class)
                9.0

        Returns float.
        '''
        return float(self._pitch_class_number)

    def __hash__(self):
        r'''Hashes numbered pitch-class.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(NumberedPitchClass, self).__hash__()

    def __int__(self):
        r'''Changes numbered pitch-class to integer.

        ..  container:: example

            ::

                >>> pitch_class = NumberedPitchClass(9)
                >>> int(pitch_class)
                9

        Returns integer.
        '''
        return self._pitch_class_number

    def __lt__(self, argument):
        r'''Is true when `argument` is a numbered pitch-class with a pitch
        number greater than that of this numberd pitch-class.

        ..  container:: example

            Compares less than:

            ::

                >>> NumberedPitchClass(1) < NumberedPitchClass(2)
                True

        ..  container:: example

            Does not compare less than:

            ::

                >>> NumberedPitchClass(2) < NumberedPitchClass(1)
                False

        Raises type error when `argument` is not a numbered pitch-class.
        '''
        if not isinstance(argument, type(self)):
            message = 'can not compare numbered pitch-class to {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        return self.pitch_class_number < argument.pitch_class_number

    def __neg__(self):
        r'''Negates numbered pitch-class.

        ..  container:: example

            ::

                >>> pitch_class = NumberedPitchClass(9)
                >>> -pitch_class
                NumberedPitchClass(3)

        Returns new numbered pitch-class.
        '''
        return type(self)(-self.pitch_class_number)

    def __str__(self):
        r'''Gets string representation of numbered pitch-class.

        Returns string.
        '''
        return str(self.pitch_class_number)

    def __sub__(self, argument):
        r'''Subtracts `argument` from numbered pitch-class.

        Subtraction defined against both numbered intervals
        and against other pitch-classes.

        Returns numbered inversion-equivalent interval-class.
        '''
        from abjad.tools import pitchtools
        if isinstance(argument, type(self)):
            interval_class_number = abs(
                self.pitch_class_number -
                argument.pitch_class_number
                )
            if 6 < interval_class_number:
                interval_class_number = 12 - interval_class_number
            return pitchtools.NumberedInversionEquivalentIntervalClass(
                interval_class_number)
        interval_class = pitchtools.NumberedInversionEquivalentIntervalClass(
            argument)
        return type(self)(self.pitch_class_number - interval_class.number % 12)

    ### PRIVATE METHODS ###

    def _initialize_by_named_pitch(self, argument):
        self._pitch_class_number = argument.pitch_class_number

    def _initialize_by_named_pitch_class(self, argument):
        self._pitch_class_number = argument.pitch_class_number

    def _initialize_by_number(self, argument):
        argument = round((float(argument) % 12) * 4) / 4
        div, mod = divmod(argument, 1)
        if mod == 0.75:
            div += 1
        elif mod == 0.5:
            div += 0.5
        div %= 12
        self._pitch_class_number = \
            mathtools.integer_equivalent_number_to_integer(div)

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
        r'''Gets accidental of numbered pitch-class.

        ..  container:: example

            ::

                >>> NumberedPitchClass(1).accidental
                Accidental('s')

        Returns accidental.
        '''
        from abjad.tools import pitchtools
        return pitchtools.Accidental(self.alteration_in_semitones)

    @property
    def alteration_in_semitones(self):
        r'''Alteration of numbered pitch-class in semitones.

        ..  container:: example

            ::

                >>> NumberedPitchClass(1).alteration_in_semitones
                1

            ::

                >>> NumberedPitchClass(10.5).alteration_in_semitones
                -0.5

        Returns integer or float.
        '''
        return (self.pitch_class_number -
            self._diatonic_pitch_class_number_to_pitch_class_number[
                self.diatonic_pitch_class_number])

    @property
    def diatonic_pitch_class_name(self):
        r'''Gets diatonic pitch-class name corresponding to numbered
        pitch-class.

        ..  container:: example

            ::

                >>> NumberedPitchClass(1).diatonic_pitch_class_name
                'c'

        Returns string.
        '''
        return self.pitch_class_name[0]

    @property
    def diatonic_pitch_class_number(self):
        r'''Gets diatonic pitch-class number corresponding to numbered
        pitch-class.

        ..  container:: example

            ::

                >>> NumberedPitchClass(1).diatonic_pitch_class_number
                0

        Returns integer.
        '''
        return self._diatonic_pitch_class_name_to_diatonic_pitch_class_number[
            self.diatonic_pitch_class_name]

    @property
    def named_pitch_class(self):
        r'''Gets named pitch-class corresponding to numbered pitch-class.

        ..  container:: example

            ::

                >>> NumberedPitchClass(13).named_pitch_class
                NamedPitchClass('cs')

        Returns named pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NamedPitchClass(self)

    @property
    def number(self):
        r'''Gets number of numbered pitch-class.

        ..  container:: example

            ::

                >>> NumberedPitchClass(1).number
                1

        ..  container:: example

            ::

                >>> NumberedPitchClass(13).number
                1

        '''
        return self._pitch_class_number

    @property
    def numbered_pitch_class(self):
        r'''Numbered pitch-class.

        ..  container:: example

            ::

                >>> NumberedPitchClass(13).numbered_pitch_class
                NumberedPitchClass(1)

        Returns new numbered pitch-class.
        '''
        return type(self)(self)

    @property
    def pitch_class_label(self):
        r'''Gets pitch-class / octave label of numbered pitch-class.

        ..  container:: example

            ::

                >>> NumberedPitchClass(13).pitch_class_label
                'C#'

        Returns string.
        '''
        return '{}{}'.format(
            self.diatonic_pitch_class_name.upper(),
            self.accidental.symbolic_string,
            )

    @property
    def pitch_class_name(self):
        r'''Gets pitch-class name.

        ..  container:: example

            ::

                >>> NumberedPitchClass(1).pitch_class_name
                'cs'

        Returns string.
        '''
        from abjad import abjad_configuration
        accidental_spelling = abjad_configuration['accidental_spelling']
        if accidental_spelling == 'mixed':
            return self._pitch_class_number_to_pitch_class_name[
                self._pitch_class_number]
        elif accidental_spelling == 'sharps':
            return self._pitch_class_number_to_pitch_class_name_with_sharps[
                self._pitch_class_number]
        elif accidental_spelling == 'flats':
            return self._pitch_class_number_to_pitch_class_name_with_flats[
                self._pitch_class_number]
        else:
            message = 'unknown accidental spelling: {!r}.'
            message = message.format(accidental_spelling)
            raise ValueError(message)

    @property
    def pitch_class_number(self):
        r'''Gets pitch-class number.

        ..  container:: example

            ::

                >>> NumberedPitchClass(1).pitch_class_number
                1

        Returns number.
        '''
        return self._pitch_class_number

    ### PUBLIC METHODS ###

    def apply_accidental(self, accidental=None):
        '''Applies `accidental` to numbered pitch-class.

        ..  container:: example

            ::

                >>> NumberedPitchClass(1).apply_accidental('flat')
                NumberedPitchClass(0)

        Returns new numbered pitch-class.
        '''
        from abjad.tools import pitchtools
        accidental = pitchtools.Accidental(accidental)
        semitones = self.pitch_class_number + accidental.semitones
        return type(self)(semitones)

    def invert(self, axis=None):
        r'''Inverts numbered pitch-class.

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

            ::

                >>> NumberedPitchClass(11).multiply(3)
                NumberedPitchClass(9)

        Returns new numbered pitch-class.
        '''
        return type(self)(self.pitch_class_number * n)

    def transpose(self, n=0):
        r'''Transposes numbered pitch-class by index `n`.

        Returns new numbered pitch-class.
        '''
        return type(self)(self.pitch_class_number + n)
