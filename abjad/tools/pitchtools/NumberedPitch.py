# -*- encoding: utf-8 -*-
import functools
from abjad.tools import mathtools
from abjad.tools.pitchtools.Pitch import Pitch


@functools.total_ordering
class NumberedPitch(Pitch):
    '''A numbered pitch.

    ::

        >>> pitchtools.NumberedPitch(13)
        NumberedPitch(13)

    Returns numbered pitch.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pitch_number',
        )

    ### INITIALIZER ###

    def __init__(self, expr):
        from abjad.tools import pitchtools
        if hasattr(expr, 'pitch_number'):
            pitch_number = expr.pitch_number
        elif Pitch.is_pitch_number(expr):
            pitch_number = expr
        else:
            pitch_number = pitchtools.NamedPitch(expr).pitch_number
        self._pitch_number = mathtools.integer_equivalent_number_to_integer(
            pitch_number)

    ### SPECIAL METHODS ###

    def __abs__(self):
        return self._pitch_number

    def __add__(self, arg):
        arg = type(self)(arg)
        semitones = abs(self) + abs(arg)
        return type(self)(semitones)

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            return self._pitch_number == expr._pitch_number
        return self._pitch_number == expr

    def __float__(self):
        return float(self._pitch_number)

    def __getnewargs__(self):
        return (self._pitch_number, )

    def __hash__(self):
        return hash(repr(self))

    def __int__(self):
        return self._pitch_number

    def __lt__(self, expr):
        if isinstance(expr, type(self)):
            return self._pitch_number < expr._pitch_number
        try:
            expr = type(self)(expr)
        except (ValueError, TypeError):
            return False
        return self._pitch_number < expr._pitch_number

    def __neg__(self):
        return type(self)(-abs(self))

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, abs(self))

    def __str__(self):
        return '%s' % abs(self)

    def __sub__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, type(self)):
            return pitchtools.NumberedInterval.from_pitch_carriers(
                self, arg)
        else:
            interval = arg
            return pitchtools.transpose_pitch_carrier_by_interval(
                self, -interval)

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        return self.pitch_name

    @property
    def _positional_argument_values(self):
        return (
            self.pitch_number,
            )

    ### PUBLIC METHODS ###

    def apply_accidental(self, accidental=None):
        r'''Apply `accidental`.

        ::

            >>> pitchtools.NumberedPitch(13).apply_accidental('flat')
            NumberedPitch(12)

        Emit new numbered pitch.
        '''
        from abjad.tools.pitchtools.Accidental import Accidental
        accidental = Accidental(accidental)
        semitones = abs(self) + accidental.semitones
        return type(self)(semitones)

    def invert(self, axis=None):
        r'''Invert around `axis`.

        Not yet implemented.
        '''
        raise NotImplementedError
    
    def multiply(self, n=1):
        r'''Multiply pitch-class by `n`, maintaining octave.
        
        ::

            >>> pitchtools.NumberedPitch(14).multiply(3)
            NumberedPitch(18)

        Emit new numbered pitch.
        '''
        pitch_class_number = (self.pitch_class_number * n) % 12
        octave_floor = (self.octave_number - 4) * 12
        return type(self)(pitch_class_number + octave_floor)

    def transpose(self, n=0):
        r'''Tranpose by `n` semitones.

        ::

            >>> pitchtools.NumberedPitch(13).transpose(1)
            NumberedPitch(14)

        Emit new numbered pitch.
        '''
        semitones = abs(self) + n
        return type(self)(semitones)

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        r'''Accidental.

        ::

            >>> pitchtools.NumberedPitchClass(13).accidental
            Accidental('s')

        Returns accidental.
        '''
        from abjad.tools import pitchtools
        return pitchtools.Accidental(self.alteration_in_semitones)

    @property
    def alteration_in_semitones(self):
        r'''Alteration in semitones.

        ::

            >>> pitchtools.NumberedPitchClass(13).alteration_in_semitones
            1

        Returns integer or float.
        '''
        return self.numbered_pitch_class.alteration_in_semitones

    @property
    def diatonic_pitch_class_name(self):
        r'''Diatonic pitch-class name.

        ::

            >>> pitchtools.NumberedPitch(13).diatonic_pitch_class_name
            'c'

        Returns string.
        '''
        return self.numbered_pitch_class.diatonic_pitch_class_name

    @property
    def diatonic_pitch_class_number(self):
        r'''Diatonic pitch-class number.

        ::

            >>> pitchtools.NumberedPitch(13).diatonic_pitch_class_number
            0

        Returns integer.
        '''
        return self.numbered_pitch_class.diatonic_pitch_class_number

    @property
    def diatonic_pitch_name(self):
        r'''Diatonic pitch name.

        ::

            >>> pitchtools.NumberedPitch(13).diatonic_pitch_name
            "c''"

        Returns string.
        '''
        return '{}{}'.format(
            self.diatonic_pitch_class_name,
            self.octave.octave_tick_string,
            )

    @property
    def diatonic_pitch_number(self):
        r'''Diatonic pitch-class number.

        ::

            >>> pitchtools.NumberedPitch(13).diatonic_pitch_number
            7

        Returns integer.
        '''
        from abjad.tools import pitchtools
        return ((self.octave_number - 4) * 7) + \
            self.diatonic_pitch_class_number

    @property
    def named_pitch(self):
        r'''Named pitch.

        ::

            >>> pitchtools.NumberedPitch(13).named_pitch
            NamedPitch("cs''")

        Returns named pitch.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NamedPitch(self)

    @property
    def named_pitch_class(self):
        r'''Named pitch-class.

        ::

            >>> pitchtools.NumberedPitch(13).named_pitch_class
            NamedPitchClass('cs')

        Returns named pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NamedPitchClass(self)

    @property
    def numbered_pitch(self):
        r'''Numbered pitch.

        ::

            >>> pitchtools.NumberedPitch(13).numbered_pitch
            NumberedPitch(13)

        Returns numbered pitch.
        '''
        return type(self)(self)

    @property
    def numbered_pitch_class(self):
        r'''Numbered pitch-class.

        ::

            >>> pitchtools.NumberedPitch(13).numbered_pitch_class
            NumberedPitchClass(1)

        Returns numbered pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClass(self)

    @property
    def octave(self):
        r'''Octave indication.

        ::

            >>> pitchtools.NumberedPitch(13).octave
            Octave(5)

        Returns octave.
        '''
        from abjad.tools import pitchtools
        return pitchtools.Octave(self.octave_number)

    @property
    def octave_number(self):
        r'''Octave number.

        ::

            >>> pitchtools.NumberedPitch(13).octave_number
            5

        Returns integer.
        '''
        return self._pitch_number // 12 + 4

    @property
    def pitch_class_name(self):
        r'''Pitch-class name.

        ::

            >>> pitchtools.NumberedPitch(13).pitch_class_name
            'cs'

        Returns string.
        '''
        return self.numbered_pitch_class.pitch_class_name

    @property
    def pitch_class_number(self):
        r'''Pitch-class number.

        ::

            >>> pitchtools.NumberedPitch(13).pitch_class_number
            1

        Returns integer or float.
        '''
        return self._pitch_number % 12

    @property
    def pitch_class_octave_label(self):
        r'''Pitch-class / octave label.

        ::

            >>> pitchtools.NumberedPitch(13).pitch_class_octave_label
            'C#5'

        Returns string.
        '''
        return '{}{}{}'.format(
            self.diatonic_pitch_class_name.upper(),
            self.accidental.symbolic_accidental_string,
            self.octave_number,
            )

    @property
    def pitch_name(self):
        r'''Pitch name.

        ::

            >>> pitchtools.NumberedPitch(13).pitch_name
            "cs''"

        Returns string.
        '''
        return '{}{}'.format(
            self.numbered_pitch_class.pitch_class_name,
            self.octave.octave_tick_string,
            )

    @property
    def pitch_number(self):
        r'''Pitch-class number.

        ::

            >>> pitchtools.NumberedPitch(13).pitch_number
            13

        Returns integer or float.
        '''
        return self._pitch_number
