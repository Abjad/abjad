# -*- coding: utf-8 -*-
import functools
import numbers
from abjad.tools import mathtools
from abjad.tools.pitchtools.PitchClass import PitchClass


@functools.total_ordering
class NumberedPitchClass(PitchClass):
    '''Numbered pitch-class.

    ..  container:: example

        **Example 1.** Initializes from number of semitones:

        ::

            >>> pitchtools.NumberedPitchClass(13)
            NumberedPitchClass(1)

    ..  container:: example

        **Example 2.** Initializes from pitch name.

        ::

            >>> pitchtools.NumberedPitchClass('d')
            NumberedPitchClass(2)

    ..  container:: example

        **Example 3.** Initializes from named pitch.

        ::

            >>> pitchtools.NumberedPitchClass(NamedPitch('g,'))
            NumberedPitchClass(7)

    ..  container:: example

        **Example 4.** Initializes from numbered pitch.

        ::

            >>> pitchtools.NumberedPitchClass(pitchtools.NumberedPitch(15))
            NumberedPitchClass(3)

    ..  container:: example

        **Example 5.** Initializes from named pitch-class.

        ::

            >>> pitchtools.NumberedPitchClass(pitchtools.NamedPitchClass('e'))
            NumberedPitchClass(4)

    ..  container:: example

        **Example 6.** Initializes from numbered pitch-class.

        ::

            >>> pitchtools.NumberedPitchClass('C#5')
            NumberedPitchClass(1)

    ..  container:: example

        **Example 7.** Initializes from numbered pitch-class.

        ::

            >>> pitchtools.NumberedPitchClass(Note("a'8."))
            NumberedPitchClass(9)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pitch_class_number',
        )

    ### INITIALIZER ###

    def __init__(self, expr=None):
        from abjad.tools import pitchtools
        prototype = (numbers.Number, pitchtools.NumberedPitch, type(self))
        if isinstance(expr, prototype):
            self._initialize_by_number(float(expr))
        elif isinstance(expr, pitchtools.NamedPitch):
            self._initialize_by_named_pitch(expr)
        elif isinstance(expr, pitchtools.NamedPitchClass):
            self._initialize_by_named_pitch_class(expr)
        elif isinstance(expr, str):
            self._initialize_by_string(expr)
        elif pitchtools.Pitch.is_pitch_carrier(expr):
            self._initialize_by_pitch_carrier(expr)
        elif expr is None:
            self._initialize_by_number(0)
        else:
            message = 'can not instantiate {}: {!r}.'
            message = message.format(type(self).__name__, expr)
            raise TypeError(message)

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        r'''Adds `expr` to numbered pitch-class.

        ::

            >>> pitch_class = pitchtools.NumberedPitchClass(9)
            >>> interval = pitchtools.NumberedInterval(4)
            >>> pitch_class + interval
            NumberedPitchClass(1)

        Returns new numbered pitch-class.
        '''
        from abjad.tools import pitchtools
        interval = pitchtools.NumberedInterval(expr)
        return type(self)(self.pitch_class_number + interval.number % 12)

    def __copy__(self, *args):
        r'''Copies numbered pitch-class.

        ::

            >>> import copy
            >>> pitch_class = pitchtools.NumberedPitchClass(9)
            >>> copy.copy(pitch_class)
            NumberedPitchClass(9)

        Returns new numbered pitch-class.
        '''
        return type(self)(self)

    def __eq__(self, arg):
        r'''Is true when `arg` is a numbered pitch-class with pitch-class number
        equal to that of this numbered pitch-class.

        ::

            >>> pitch_class_1 = pitchtools.NumberedPitchClass(9)
            >>> pitch_class_2 = pitchtools.NumberedPitchClass(3)
            >>> pitch_class_1 == pitch_class_1
            True

        Otherwise false:

        ::

            >>> pitch_class_1 == pitch_class_2
            False

        Returns true or false.
        '''
        if isinstance(arg, type(self)):
            return self._pitch_class_number == \
                arg._pitch_class_number
        return self._pitch_class_number == arg

    def __float__(self):
        r'''Changes numbered pitch-class to float.

        ::

            >>> pitch_class = pitchtools.NumberedPitchClass(9)
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

        ::

            >>> pitch_class = pitchtools.NumberedPitchClass(9)
            >>> int(pitch_class)
            9

        Returns integer.
        '''
        return self._pitch_class_number

    def __lt__(self, expr):
        r'''Is true when `expr` is a numbered pitch-class with a pitch number
        greater than that of this numberd pitch-class.

        ..  container:: example

            **Example 1.** Compares less than:

            ::

                >>> pitchtools.NumberedPitchClass(1) < pitchtools.NumberedPitchClass(2)
                True

        ..  container:: example

            **Example 2.** Does not compare less than:

            ::

                >>> pitchtools.NumberedPitchClass(2) < pitchtools.NumberedPitchClass(1)
                False

        Raises type error when `expr` is not a numbered pitch-class.
        '''
        if not isinstance(expr, type(self)):
            message = 'can not compare numbered pitch-class to {!r}.'
            message = message.format(expr)
            raise TypeError(message)
        return self.pitch_class_number < expr.pitch_class_number

    def __neg__(self):
        r'''Negates numbered pitch-class.

        ::

            >>> pitch_class = pitchtools.NumberedPitchClass(9)
            >>> -pitch_class
            NumberedPitchClass(3)

        Returns new numbered pitch-class.
        '''
        return type(self)(-self.pitch_class_number)

    def __str__(self):
        r'''String representation of numbered pitch-class.

        Returns string.
        '''
        return str(self.pitch_class_number)

    def __sub__(self, expr):
        r'''Subtracts `expr` from numbered pitch-class.

        Subtraction defined against both numbered intervals
        and against other pitch-classes.

        Returns numbered inversion-equivalent interval-class.
        '''
        from abjad.tools import pitchtools
        if isinstance(expr, type(self)):
            interval_class_number = abs(
                self.pitch_class_number -
                expr.pitch_class_number
                )
            if 6 < interval_class_number:
                interval_class_number = 12 - interval_class_number
            return pitchtools.NumberedInversionEquivalentIntervalClass(
                interval_class_number)
        interval_class = pitchtools.NumberedInversionEquivalentIntervalClass(
            expr)
        return type(self)(self.pitch_class_number - interval_class.number % 12)

    ### PRIVATE METHODS ###

    def _initialize_by_named_pitch(self, expr):
        self._pitch_class_number = expr.pitch_class_number

    def _initialize_by_named_pitch_class(self, expr):
        self._pitch_class_number = expr.pitch_class_number

    def _initialize_by_number(self, expr):
        expr = round((float(expr) % 12) * 4) / 4
        div, mod = divmod(expr, 1)
        if mod == 0.75:
            div += 1
        elif mod == 0.5:
            div += 0.5
        div %= 12
        self._pitch_class_number = \
            mathtools.integer_equivalent_number_to_integer(div)

    def _initialize_by_pitch_carrier(self, expr):
        from abjad.tools import pitchtools
        named_pitch = pitchtools.NamedPitch.from_pitch_carrier(expr)
        self._initialize_by_named_pitch(named_pitch)

    def _initialize_by_string(self, expr):
        from abjad.tools import pitchtools
        named_pitch_class = pitchtools.NamedPitchClass(expr)
        self._initialize_by_named_pitch_class(named_pitch_class)

    ### PUBLIC METHODS ###

    def apply_accidental(self, accidental=None):
        '''Applies `accidental` to numbered pitch-class.

        ::

            >>> pitchtools.NumberedPitchClass(1).apply_accidental('flat')
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

        ::

            >>> pitchtools.NumberedPitchClass(11).multiply(3)
            NumberedPitchClass(9)

        Returns new numbered pitch-class.
        '''
        return type(self)(self.pitch_class_number * n)

    def transpose(self, n):
        r'''Transposes numbered pitch-class by `n` semitones.

        Returns new numbered pitch-class.
        '''
        return type(self)(self.pitch_class_number + n)

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        r'''Accidental of numbered pitch-class.

        ::

            >>> pitchtools.NumberedPitchClass(1).accidental
            Accidental('s')

        Returns accidental.
        '''
        from abjad.tools import pitchtools
        return pitchtools.Accidental(self.alteration_in_semitones)

    @property
    def alteration_in_semitones(self):
        r'''Alteration of numbered pitch-class in semitones.

        ::

            >>> pitchtools.NumberedPitchClass(1).alteration_in_semitones
            1

        ::

            >>> pitchtools.NumberedPitchClass(10.5).alteration_in_semitones
            -0.5

        Returns integer or float.
        '''
        return (self.pitch_class_number -
            self._diatonic_pitch_class_number_to_pitch_class_number[
                self.diatonic_pitch_class_number])

    @property
    def diatonic_pitch_class_name(self):
        r'''Diatonic pitch-class name corresponding to numbered pitch-class.

        ::

            >>> pitchtools.NumberedPitchClass(1).diatonic_pitch_class_name
            'c'

        Returns string.
        '''
        return self.pitch_class_name[0]

    @property
    def diatonic_pitch_class_number(self):
        r'''Diatonic pitch-class number corresponding to numbered pitch-class.

        ::

            >>> pitchtools.NumberedPitchClass(1).diatonic_pitch_class_number
            0

        Returns integer.
        '''
        return self._diatonic_pitch_class_name_to_diatonic_pitch_class_number[
            self.diatonic_pitch_class_name]

    @property
    def named_pitch_class(self):
        r'''Named pitch-class corresponding to numbered pitch-class.

        ::

            >>> pitchtools.NumberedPitchClass(13).named_pitch_class
            NamedPitchClass('cs')

        Returns named pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NamedPitchClass(self)

    @property
    def numbered_pitch_class(self):
        r'''Numbered pitch-class.

        ::

            >>> pitchtools.NumberedPitchClass(13).numbered_pitch_class
            NumberedPitchClass(1)

        Returns new numbered pitch-class.
        '''
        return type(self)(self)

    @property
    def pitch_class_label(self):
        r'''Pitch-class / octave label of numbered pitch-class.

        ::

            >>> pitchtools.NumberedPitchClass(13).pitch_class_label
            'C#'

        Returns string.
        '''
        return '{}{}'.format(
            self.diatonic_pitch_class_name.upper(),
            self.accidental.symbolic_string,
            )

    @property
    def pitch_class_name(self):
        r'''Pitch-class name.

        ::

            >>> pitchtools.NumberedPitchClass(1).pitch_class_name
            'cs'

        Returns string.
        '''
        if self.accidental_spelling == 'mixed':
            return self._pitch_class_number_to_pitch_class_name[
                self._pitch_class_number]
        elif self.accidental_spelling == 'sharps':
            return self._pitch_class_number_to_pitch_class_name_with_sharps[
                self._pitch_class_number]
        elif self.accidental_spelling == 'flats':
            return self._pitch_class_number_to_pitch_class_name_with_flats[
                self._pitch_class_number]
        else:
            raise ValueError

    @property
    def pitch_class_number(self):
        r'''Pitch-class number.

        ::

            >>> pitchtools.NumberedPitchClass(1).pitch_class_number
            1

        Returns number.
        '''
        return self._pitch_class_number
