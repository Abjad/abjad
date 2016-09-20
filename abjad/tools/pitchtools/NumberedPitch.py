# -*- coding: utf-8 -*-
import functools
from abjad.tools import mathtools
from abjad.tools.pitchtools.Pitch import Pitch


@functools.total_ordering
class NumberedPitch(Pitch):
    '''Numbered pitch.

    ..  container:: example

        **Example 1.** Initializes from pitch number:

        ::

            >>> numbered_pitch = pitchtools.NumberedPitch(13)
            >>> numbered_pitch
            NumberedPitch(13)

        ::

            >>> show(numbered_pitch) # doctest: +SKIP

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pitch_number',
        )

    ### INITIALIZER ###

    def __init__(self, pitch_number=None):
        from abjad.tools import pitchtools
        if hasattr(pitch_number, 'pitch_number'):
            pitch_number = pitch_number.pitch_number
        elif Pitch.is_pitch_number(pitch_number):
            pitch_number = pitch_number
        elif pitch_number is None:
            pitch_number = 0
        else:
            pitch_number = pitchtools.NamedPitch(pitch_number).pitch_number
        pitch_number = mathtools.integer_equivalent_number_to_integer(
            pitch_number)
        self._pitch_number = pitch_number

    ### SPECIAL METHODS ###

    def __add__(self, arg):
        r'''Adds `arg` to numberd pitch.

        Returns new numbered pitch.
        '''
        arg = type(self)(arg)
        semitones = self.pitch_number + arg.pitch_number
        return type(self)(semitones)

    def __float__(self):
        r'''Changes numbered pitch to float.

        Returns float.
        '''
        return float(self._pitch_number)

    def __int__(self):
        r'''Changes numbered pitch to integer.

        Returns integer.
        '''
        return self._pitch_number

    def __lt__(self, arg):
        r'''Is true when `arg` can be coerced to a numbered pitch and when this
        numbered pitch is less than `arg`. Otherwise false.

        Returns true or false.
        '''
        try:
            arg = type(self)(arg)
        except (ValueError, TypeError):
            return False
        return self.pitch_number < arg.pitch_number

    def __neg__(self):
        r'''Negates numbered pitch.

        Returns new numbered pitch.
        '''
        return type(self)(-self.pitch_number)

    def __str__(self):
        r'''String representation of numbered pitch.

        Returns string.
        '''
        return str(self.pitch_number)

    def __sub__(self, arg):
        r'''Subtracts `arg` from numbered pitch.

        Returns numbered interval.
        '''
        from abjad.tools import pitchtools
        if isinstance(arg, type(self)):
            return pitchtools.NumberedInterval.from_pitch_carriers(
                self, arg)
        else:
            interval = arg
            return pitchtools.transpose_pitch_carrier_by_interval(
                self, -interval)

    ### PUBLIC METHODS ###

    def apply_accidental(self, accidental=None):
        r'''Applies `accidental` to numbered pitch.

        ::

            >>> pitchtools.NumberedPitch(13).apply_accidental('flat')
            NumberedPitch(12)

        Returns new numbered pitch.
        '''
        from abjad.tools.pitchtools.Accidental import Accidental
        accidental = Accidental(accidental)
        semitones = self.pitch_number + accidental.semitones
        return type(self)(semitones)

    def interpolate(self, stop_pitch, fraction):
        r'''Interpolates between this pitch and `stop_pitch`
        by `fraction` amount.

        ..  container:: example

            **Example 1.** Interpolates up from C4 to C5:

            ::

                >>> start_pitch = pitchtools.NumberedPitch(0)
                >>> stop_pitch = pitchtools.NumberedPitch(12)

            ::

                >>> start_pitch.interpolate(stop_pitch, Fraction(0))
                NumberedPitch(0)
                >>> start_pitch.interpolate(stop_pitch, Fraction(1, 4))
                NumberedPitch(3)
                >>> start_pitch.interpolate(stop_pitch, Fraction(1, 2))
                NumberedPitch(6)
                >>> start_pitch.interpolate(stop_pitch, Fraction(3, 4))
                NumberedPitch(9)
                >>> start_pitch.interpolate(stop_pitch, Fraction(1))
                NumberedPitch(12)

        ..  container:: example

            **Example 2.** Interpolates down from C5 to C4:

            ::

                >>> start_pitch = pitchtools.NumberedPitch(12)
                >>> stop_pitch = pitchtools.NumberedPitch(0)

            ::

                >>> start_pitch.interpolate(stop_pitch, Fraction(0))
                NumberedPitch(12)
                >>> start_pitch.interpolate(stop_pitch, Fraction(1, 4))
                NumberedPitch(9)
                >>> start_pitch.interpolate(stop_pitch, Fraction(1, 2))
                NumberedPitch(6)
                >>> start_pitch.interpolate(stop_pitch, Fraction(3, 4))
                NumberedPitch(3)
                >>> start_pitch.interpolate(stop_pitch, Fraction(1))
                NumberedPitch(0)

        Returns new pitch.
        '''
        from abjad.tools import pitchtools
        assert 0 <= fraction <= 1, repr(fraction)
        stop_pitch = type(self)(stop_pitch)
        distance = stop_pitch - self
        distance = abs(distance.semitones)
        distance = fraction * distance
        distance = int(distance)
        if stop_pitch < self:
            distance *= -1
        pitch_number = self.pitch_number
        pitch_number = pitch_number + distance
        pitch = pitchtools.NumberedPitch(pitch_number)
        if self <= stop_pitch:
            triple = (self, pitch, stop_pitch)
            assert self <= pitch <= stop_pitch, triple
        else:
            triple = (self, pitch, stop_pitch)
            assert self >= pitch >= stop_pitch, triple
        return pitch

    def invert(self, axis=None):
        r'''Inverts numberd pitch around `axis`.

        ..  container:: example

            **Example 1.** Inverts pitch-class about pitch-class 0 explicitly:

            ::

                >>> pitchtools.NumberedPitch(2).invert(0)
                NumberedPitch(-2)

            ::

                >>> pitchtools.NumberedPitch(-2).invert(0)
                NumberedPitch(2)

            Default behavior.

            **Example 2.** Inverts pitch-class about pitch-class 0 implicitly:

            ::

                >>> pitchtools.NumberedPitch(2).invert()
                NumberedPitch(-2)

            ::

                >>> pitchtools.NumberedPitch(-2).invert()
                NumberedPitch(2)

            Default behavior.

            **Example 3.** Inverts pitch-class about pitch-class -3:

            ::

                >>> pitchtools.NumberedPitch(2).invert(-3)
                NumberedPitch(-8)

        Returns new numbered pitch.
        '''
        return Pitch.invert(self, axis=axis)

    def multiply(self, n=1):
        r'''Multiplies pitch-class of numbered pitch by `n` and maintains
        octave.

        ::

            >>> pitchtools.NumberedPitch(14).multiply(3)
            NumberedPitch(18)

        Returns new numbered pitch.
        '''
        pitch_class_number = (self.pitch_class_number * n) % 12
        octave_floor = (self.octave_number - 4) * 12
        return type(self)(pitch_class_number + octave_floor)

    def transpose(self, n=0):
        r'''Tranposes numbered pitch by `n` semitones.

        ::

            >>> pitchtools.NumberedPitch(13).transpose(1)
            NumberedPitch(14)

        Returns new numbered pitch.
        '''
        semitones = self.pitch_number + float(n)
        return type(self)(semitones)

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        return self.pitch_name

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        r'''Accidental of numbered pitch.

        ::

            >>> pitchtools.NumberedPitchClass(13).accidental
            Accidental('s')

        Returns accidental.
        '''
        from abjad.tools import pitchtools
        return pitchtools.Accidental(self.alteration_in_semitones)

    @property
    def alteration_in_semitones(self):
        r'''Alteration of numbered pitch in semitones.

        ::

            >>> pitchtools.NumberedPitchClass(13).alteration_in_semitones
            1

        Returns integer or float.
        '''
        return self.numbered_pitch_class.alteration_in_semitones

    @property
    def diatonic_pitch_class_name(self):
        r'''Diatonic pitch-class name corresponding to numbered pitch.

        ::

            >>> pitchtools.NumberedPitch(13).diatonic_pitch_class_name
            'c'

        Returns string.
        '''
        return self.numbered_pitch_class.diatonic_pitch_class_name

    @property
    def diatonic_pitch_class_number(self):
        r'''Diatonic pitch-class number of numbered pitch.

        ::

            >>> pitchtools.NumberedPitch(13).diatonic_pitch_class_number
            0

        Returns integer.
        '''
        return self.numbered_pitch_class.diatonic_pitch_class_number

    @property
    def diatonic_pitch_name(self):
        r'''Diatonic pitch name of numbered pitch.

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
        r'''Diatonic pitch-class number corresponding to numbered pitch.

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
        r'''Named pitch corresponding to numbered pitch.

        ::

            >>> pitchtools.NumberedPitch(13).named_pitch
            NamedPitch("cs''")

        Returns named pitch.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NamedPitch(self)

    @property
    def named_pitch_class(self):
        r'''Named pitch-class corresponding to numbered pitch.

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

        Returns new numbered pitch.
        '''
        return type(self)(self)

    @property
    def numbered_pitch_class(self):
        r'''Numbered pitch-class corresponding to numbered pitch.

        ::

            >>> pitchtools.NumberedPitch(13).numbered_pitch_class
            NumberedPitchClass(1)

        Returns numbered pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClass(self)

    @property
    def octave(self):
        r'''Octave of numbered pitch.

        ::

            >>> pitchtools.NumberedPitch(13).octave
            Octave(5)

        Returns octave.
        '''
        from abjad.tools import pitchtools
        return pitchtools.Octave(self.octave_number)

    @property
    def octave_number(self):
        r'''Octave number of numbered pitch.

        ::

            >>> pitchtools.NumberedPitch(13).octave_number
            5

        Returns integer.
        '''
        return self._pitch_number // 12 + 4

    @property
    def pitch_class_name(self):
        r'''Pitch-class name of numbered pitch.

        ::

            >>> pitchtools.NumberedPitch(13).pitch_class_name
            'cs'

        Returns string.
        '''
        return self.numbered_pitch_class.pitch_class_name

    @property
    def pitch_class_number(self):
        r'''Pitch-class number of numbered pitch.

        ::

            >>> pitchtools.NumberedPitch(13).pitch_class_number
            1

        Returns integer or float.
        '''
        return self._pitch_number % 12

    @property
    def pitch_class_octave_label(self):
        r'''Pitch-class / octave label of numbered pitch.

        ::

            >>> pitchtools.NumberedPitch(13).pitch_class_octave_label
            'C#5'

        Returns string.
        '''
        return '{}{}{}'.format(
            self.diatonic_pitch_class_name.upper(),
            self.accidental.symbolic_string,
            self.octave_number,
            )

    @property
    def pitch_name(self):
        r'''Pitch name corresponding to numbered pitch.

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
        r'''Pitch number of numbered pitch.

        ::

            >>> pitchtools.NumberedPitch(13).pitch_number
            13

        Returns number.
        '''
        return self._pitch_number
