# -*- encoding: utf-8 -*-
import numbers
from abjad.tools import mathtools
from abjad.tools.pitchtools.PitchClass import PitchClass


class NumberedPitchClass(PitchClass):
    '''A numbered pitch-class.

    ::

        >>> pitchtools.NumberedPitchClass(13)
        NumberedPitchClass(1)

    ::

        >>> pitchtools.NumberedPitchClass('d')
        NumberedPitchClass(2)

    ::

        >>> pitchtools.NumberedPitchClass(NamedPitch('g,'))
        NumberedPitchClass(7)

    ::

        >>> pitchtools.NumberedPitchClass(pitchtools.NumberedPitch(15))
        NumberedPitchClass(3)

    ::

        >>> pitchtools.NumberedPitchClass(pitchtools.NamedPitchClass('e'))
        NumberedPitchClass(4)

    ::

        >>> pitchtools.NumberedPitchClass('C#5')
        NumberedPitchClass(1)

    ::

        >>> pitchtools.NumberedPitchClass(Note("a'8."))
        NumberedPitchClass(9)

    Returns numbered pitch-class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pitch_class_number',
        )

    ### INITIALIZER ###

    def __init__(self, expr):
        from abjad.tools import pitchtools
        if isinstance(expr, (
            numbers.Number,
            pitchtools.NumberedPitch,
            type(self),
            )):
            self._init_by_number(float(expr))
        elif isinstance(expr, pitchtools.NamedPitch):
            self._init_by_named_pitch(expr)
        elif isinstance(expr, pitchtools.NamedPitchClass):
            self._init_by_named_pitch_class(expr)
        elif isinstance(expr, str):
            self._init_by_string(expr)
        elif pitchtools.Pitch.is_pitch_carrier(expr):
            self._init_by_pitch_carrier(expr)
        else:
            message = 'cannot instantiate {} from ' '{!r}.'
            message = message.format(type(self).__name__, expr)
            raise TypeError(message)

    ### SPECIAL METHODS ###

    def __abs__(self):
        return self._pitch_class_number

    def __add__(self, expr):
        r'''Addition defined against numbered intervals only.
        '''
        from abjad.tools import pitchtools
        interval = pitchtools.NumberedInterval(expr)
        return type(self)(abs(self) + interval.number % 12)

    def __copy__(self, *args):
        return type(self)(self)

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            return self._pitch_class_number == \
                expr._pitch_class_number
        return self._pitch_class_number == expr

    def __float__(self):
        return float(self._pitch_class_number)

    def __int__(self):
        return self._pitch_class_number

    def __neg__(self):
        return type(self)(-abs(self))

    def __str__(self):
        return str(abs(self))

    def __sub__(self, expr):
        r'''Subtraction defined against both numbered intervals
        and against other pitch-classes.
        '''
        from abjad.tools import pitchtools
        if isinstance(expr, type(self)):
            interval_class_number = abs(abs(self) - abs(expr))
            if 6 < interval_class_number:
                interval_class_number = 12 - interval_class_number
            return pitchtools.NumberedInversionEquivalentIntervalClass(
                interval_class_number)
        interval_class = pitchtools.NumberedInversionEquivalentIntervalClass(
            expr)
        return type(self)(abs(self) - interval_class.number % 12)

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            positional_argument_values=(
                self.pitch_class_number,
                )
            )

    ### PRIVATE METHODS ###

    def _init_by_named_pitch(self, expr):
        self._pitch_class_number = expr.pitch_class_number

    def _init_by_named_pitch_class(self, expr):
        self._pitch_class_number = expr.pitch_class_number

    def _init_by_number(self, expr):
        self._pitch_class_number = \
            mathtools.integer_equivalent_number_to_integer(
                round((float(expr) % 12) * 2) / 2)

    def _init_by_pitch_carrier(self, expr):
        from abjad.tools import pitchtools
        named_pitch = pitchtools.get_named_pitch_from_pitch_carrier(
            expr)
        self._init_by_named_pitch(named_pitch)

    def _init_by_string(self, expr):
        from abjad.tools import pitchtools
        named_pitch_class = pitchtools.NamedPitchClass(expr)
        self._init_by_named_pitch_class(named_pitch_class)

    ### PUBLIC METHODS ###

    def apply_accidental(self, accidental=None):
        '''Apply `accidental`.

        ::

            >>> pitchtools.NumberedPitchClass(1).apply_accidental('flat')
            NumberedPitchClass(0)

        Emit new numbered pitch-class.
        '''
        from abjad.tools import pitchtools
        accidental = pitchtools.Accidental(accidental)
        semitones = abs(self) + accidental.semitones
        return type(self)(semitones)

    def invert(self):
        r'''Invert pitch-class.

        Emit new numbered pitch-class.
        '''
        return type(self)(12 - abs(self))

    def multiply(self, n=1):
        r'''Multiply pitch-class number by `n`:

        ::

            >>> pitchtools.NumberedPitchClass(11).multiply(3)
            NumberedPitchClass(9)

        Emit new numbered pitch-class.
        '''
        return type(self)(self.pitch_class_number * n)

    def transpose(self, n):
        r'''Transpose pitch-class by n.

        Emit new numbered pitch-class.
        '''
        return type(self)(abs(self) + n)

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        r'''Accidental.

        ::

            >>> pitchtools.NumberedPitchClass(1).accidental
            Accidental('s')

        Returns accidental.
        '''
        from abjad.tools import pitchtools
        return pitchtools.Accidental(self.alteration_in_semitones)

    @property
    def alteration_in_semitones(self):
        r'''Alteration in semitones.

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
        r'''Diatonic pitch-class name.

        ::

            >>> pitchtools.NumberedPitchClass(1).diatonic_pitch_class_name
            'c'

        Returns string.
        '''
        return self.pitch_class_name[0]

    @property
    def diatonic_pitch_class_number(self):
        r'''Diatonic pitch-class number.

        ::

            >>> pitchtools.NumberedPitchClass(1).diatonic_pitch_class_number
            0

        Returns integer.
        '''
        return self._diatonic_pitch_class_name_to_diatonic_pitch_class_number[
            self.diatonic_pitch_class_name]

    @property
    def named_pitch_class(self):
        r'''Named pitch-class.

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

        Returns numbered pitch-class.
        '''
        return type(self)(self)

    @property
    def pitch_class_label(self):
        r'''Pitch-class / octave label.

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

        Returns integer or float.
        '''
        return self._pitch_class_number
