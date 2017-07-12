# -*- coding: utf-8 -*-
import functools
from abjad.tools import mathtools
from abjad.tools.pitchtools.Pitch import Pitch


@functools.total_ordering
class NumberedPitch(Pitch):
    '''Numbered pitch.

    ::

        >>> import abjad

    ..  container:: example

        Initializes from number:

        ::

            >>> numbered_pitch = abjad.NumberedPitch(13)
            >>> show(numbered_pitch) # doctest: +SKIP

    ..  container:: example

        Initializes from other numbered pitch

        ::

            >>> numbered_pitch = abjad.NumberedPitch(abjad.NumberedPitch(13))
            >>> show(numbered_pitch) # doctest: +SKIP

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pitch_number',
        )

    ### INITIALIZER ###

    def __init__(self, pitch_number=None, arrow=None):
        from abjad.tools import pitchtools
        try:
            pitch_number = pitch_number.pitch_number
        except AttributeError:
            pass
        if Pitch.is_pitch_number(pitch_number):
            pitch_number = pitch_number
        elif pitch_number is None:
            pitch_number = 0
        else:
            pitch_number = pitchtools.NamedPitch(pitch_number).pitch_number
        pitch_number = mathtools.integer_equivalent_number_to_integer(
            pitch_number)
        self._pitch_number = pitch_number
        if arrow not in (Up, Down, None):
            message = 'arrow must be up, down or none: {!r}.'
            message = message.format(arrow)
            raise TypeError(message)
        self._arrow = arrow

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        r'''Adds `argument` to numberd pitch.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(12) + abjad.NumberedPitch(13)
                NumberedPitch(25)

            ::

                >>> abjad.NumberedPitch(13) + abjad.NumberedPitch(12)
                NumberedPitch(25)

        Returns new numbered pitch.
        '''
        argument = type(self)(argument)
        semitones = self.pitch_number + argument.pitch_number
        return type(self)(semitones)

    def __float__(self):
        r'''Changes numbered pitch to float.

        ..  container:: example

            ::

                >>> float(abjad.NumberedPitch(13))
                13.0

            ::

                >>> float(abjad.NumberedPitch(13.5))
                13.5

        Returns float.
        '''
        return float(self._pitch_number)

    def __int__(self):
        r'''Changes numbered pitch to integer.

        ..  container:: example

            ::

                >>> int(abjad.NumberedPitch(13))
                13
                
        Returns integer.
        '''
        return self._pitch_number

    def __lt__(self, argument):
        r'''Is true when `argument` can be coerced to a numbered pitch and when this
        numbered pitch is less than `argument`. Otherwise false.

        ..  container:: example

            ::

                >>> pitch_1 = abjad.NumberedPitch(12)
                >>> pitch_2 = abjad.NumberedPitch(12)
                >>> pitch_3 = abjad.NumberedPitch(13)

            ::

                >>> pitch_1 < pitch_1
                False

            ::

                >>> pitch_1 < pitch_2
                False

            ::

                >>> pitch_1 < pitch_3
                True

            ::

                >>> pitch_2 < pitch_1
                False

            ::

                >>> pitch_2 < pitch_2
                False

            ::

                >>> pitch_2 < pitch_3
                True

            ::

                >>> pitch_3 < pitch_1
                False

            ::

                >>> pitch_3 < pitch_2
                False

            ::

                >>> pitch_3 < pitch_3
                False

        Returns true or false.
        '''
        try:
            argument = type(self)(argument)
        except (ValueError, TypeError):
            return False
        return self.pitch_number < argument.pitch_number

    def __neg__(self):
        r'''Negates numbered pitch.

        ..  container:: example

            ::

                >>> -abjad.NumberedPitch(13.5)
                NumberedPitch(-13.5)

            ::

                >>> -abjad.NumberedPitch(-13.5)
                NumberedPitch(13.5)

        Returns new numbered pitch.
        '''
        return type(self)(-self.pitch_number)

    def __str__(self):
        r'''String representation of numbered pitch.

        Returns string.
        '''
        return str(self.pitch_number)

    def __sub__(self, argument):
        r'''Subtracts `argument` from numbered pitch.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(12) - abjad.NumberedPitch(12)
                NumberedInterval(0)

            ::

                >>> abjad.NumberedPitch(12) - abjad.NumberedPitch(13)
                NumberedInterval(1)

            ::

                >>> abjad.NumberedPitch(13) - abjad.NumberedPitch(12)
                NumberedInterval(-1)

        Returns numbered interval.
        '''
        from abjad.tools import pitchtools
        if isinstance(argument, type(self)):
            return pitchtools.NumberedInterval.from_pitch_carriers(
                self, argument)
        interval = pitchtools.NumberedInterval(argument)
        interval = -interval
        return interval.transpose(self)

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return self.pitch_name

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        r'''Gets accidental of numbered pitch.

        ..  container:: example

            ::

                >>> abjad.NumberedPitchClass(13).accidental
                Accidental('s')

        Returns accidental.
        '''
        from abjad.tools import pitchtools
        return pitchtools.Accidental(self.alteration_in_semitones)

    @property
    def alteration_in_semitones(self):
        r'''Gets alteration of numbered pitch in semitones.

        ..  container:: example

            ::

                >>> abjad.NumberedPitchClass(13).alteration_in_semitones
                1

        Returns integer or float.
        '''
        return self.numbered_pitch_class.alteration_in_semitones

    @property
    def arrow(self):
        r'''Gets arrow of numbered pitch.

        ..  container:: example

            Gets no arrow:

            ::

                >>> abjad.NumberedPitch(13).arrow is None
                True

        ..  container:: example

            Gets up-arrow:

            ::

                >>> abjad.NumberedPitch(13, arrow=Up).arrow
                Up

        ..  container:: example

            Gets down-arrow:

            ::

                >>> abjad.NumberedPitch(13, arrow=Down).arrow
                Down

        Returns up, down or none.
        '''
        return self._arrow

    @property
    def diatonic_pitch_class_name(self):
        r'''Gets diatonic pitch-class name corresponding to numbered pitch.

        ..  note:: Deprecated.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).diatonic_pitch_class_name
                'c'

        Returns string.
        '''
        return self.numbered_pitch_class.diatonic_pitch_class_name

    @property
    def diatonic_pitch_class_number(self):
        r'''Gets diatonic pitch-class number of numbered pitch.

        ..  note:: Deprecated.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(12).diatonic_pitch_class_number
                0

            ::

                >>> abjad.NumberedPitch(12.5).diatonic_pitch_class_number
                0

            ::

                >>> abjad.NumberedPitch(13).diatonic_pitch_class_number
                0

            ::

                >>> abjad.NumberedPitch(13.5).diatonic_pitch_class_number
                1

        Returns integer.
        '''
        return self.numbered_pitch_class.diatonic_pitch_class_number

    @property
    def diatonic_pitch_name(self):
        r'''Gets diatonic pitch name of numbered pitch.

        ..  note:: Deprecated.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).diatonic_pitch_name
                "c''"

        Returns string.
        '''
        return '{}{}'.format(
            self.diatonic_pitch_class_name,
            self.octave.tick_string,
            )

    @property
    def diatonic_pitch_number(self):
        r'''Gets diatonic pitch-class number corresponding to numbered pitch.

        ..  note:: Deprecated.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).diatonic_pitch_number
                7

        Returns integer.
        '''
        return 7 * (self.octave.number - 4) + self.diatonic_pitch_class_number

    @property
    def name(self):
        r'''Gets pitch name.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).name
                "cs''"

        Returns string
        '''
        from abjad.tools import pitchtools
        return pitchtools.NamedPitch(self).name

    @property
    def named_pitch(self):
        r'''Gets named pitch corresponding to numbered pitch.

        ..  note:: Deprecated.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).named_pitch
                NamedPitch("cs''")

        Returns named pitch.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NamedPitch(self)

    @property
    def named_pitch_class(self):
        r'''Gets named pitch-class corresponding to numbered pitch.

        ..  note:: Deprecated.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).named_pitch_class
                NamedPitchClass('cs')

        Returns named pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NamedPitchClass(self)

    @property
    def number(self):
        r'''Gets pitch number.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).number
                13

        Returns number.
        '''
        return self._pitch_number

    @property
    def numbered_pitch(self):
        r'''Gets numbered pitch.

        ..  note:: Deprecated.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).numbered_pitch
                NumberedPitch(13)

        Returns new numbered pitch.
        '''
        return type(self)(self)

    @property
    def numbered_pitch_class(self):
        r'''Gets numbered pitch-class corresponding to numbered pitch.

        ..  note:: Deprecated.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).numbered_pitch_class
                NumberedPitchClass(1)

        Returns numbered pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClass(self)

    @property
    def octave(self):
        r'''Gets octave of numbered pitch.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).octave
                Octave(5)

        Returns octave.
        '''
        from abjad.tools import pitchtools
        number = self._pitch_number // 12 + 4
        return pitchtools.Octave(number=number)

    @property
    def pitch_class(self):
        r'''Gets pitch-class.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).pitch_class
                NumberedPitchClass(1)

        Returns numbered pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClass(self)

    @property
    def pitch_class_name(self):
        r'''Gets pitch-class name of numbered pitch.

        ..  note:: Deprecated.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).pitch_class_name
                'cs'

        Returns string.
        '''
        return self.numbered_pitch_class.pitch_class_name

    @property
    def pitch_class_number(self):
        r'''Gets pitch-class number of numbered pitch.

        ..  note:: Deprecated.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).pitch_class_number
                1

        Returns integer or float.
        '''
        return self._pitch_number % 12

    @property
    def pitch_class_octave_label(self):
        r'''Gets pitch-class / octave label of numbered pitch.

        ..  note:: Deprecated.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).pitch_class_octave_label
                'C#5'

        Returns string.
        '''
        return '{}{}{}'.format(
            self.diatonic_pitch_class_name.upper(),
            self.accidental.symbolic_string,
            self.octave.number,
            )

    @property
    def pitch_name(self):
        r'''Gets pitch name corresponding to numbered pitch.

        ..  note:: Deprecated.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).pitch_name
                "cs''"

        Returns string.
        '''
        return '{}{}'.format(
            self.numbered_pitch_class.pitch_class_name,
            self.octave.tick_string,
            )

    @property
    def pitch_number(self):
        r'''Gets pitch number of numbered pitch.

        ..  note:: Deprecated.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).pitch_number
                13

        Returns number.
        '''
        return self._pitch_number

    ### PUBLIC METHODS ###

    def apply_accidental(self, accidental=None):
        r'''Applies `accidental` to numbered pitch.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).apply_accidental('flat')
                NumberedPitch(12)

            ::

                >>> abjad.NumberedPitch(13).apply_accidental('qf')
                NumberedPitch(12.5)

        Returns new numbered pitch.
        '''
        from abjad.tools.pitchtools.Accidental import Accidental
        accidental = Accidental(accidental)
        semitones = self.pitch_number + accidental.semitones
        return type(self)(semitones)

    @staticmethod
    def from_pitch_class_octave(pitch_class, octave):
        r'''Initializes numbered pitch from `pitch_class` and `octave`.

        ..  container:: example

            ::

                >>> for octave in [1, 2, 3, 4, 5, 6, 7]:
                ...     abjad.NumberedPitch.from_pitch_class_octave(6, octave)
                ...
                NumberedPitch(-30)
                NumberedPitch(-18)
                NumberedPitch(-6)
                NumberedPitch(6)
                NumberedPitch(18)
                NumberedPitch(30)
                NumberedPitch(42)

        Returns new numbered pitch.
        '''
        from abjad.tools import pitchtools
        pitch_class = pitchtools.NumberedPitchClass(pitch_class)
        octave = pitchtools.Octave(octave)
        number = 12 * (octave.number - 4) + pitch_class.number
        return NumberedPitch(number)

    def interpolate(self, stop_pitch, fraction):
        r'''Interpolates between this pitch and `stop_pitch` by `fraction`
        amount.

        ..  container:: example

            Interpolates up from C4 to C5:

            ::

                >>> start_pitch = abjad.NumberedPitch(0)
                >>> stop_pitch = abjad.NumberedPitch(12)

            ::

                >>> start_pitch.interpolate(stop_pitch, abjad.Fraction(0))
                NumberedPitch(0)
                >>> start_pitch.interpolate(stop_pitch, abjad.Fraction(1, 4))
                NumberedPitch(3)
                >>> start_pitch.interpolate(stop_pitch, abjad.Fraction(1, 2))
                NumberedPitch(6)
                >>> start_pitch.interpolate(stop_pitch, abjad.Fraction(3, 4))
                NumberedPitch(9)
                >>> start_pitch.interpolate(stop_pitch, abjad.Fraction(1))
                NumberedPitch(12)

        ..  container:: example

            Interpolates down from C5 to C4:

            ::

                >>> start_pitch = abjad.NumberedPitch(12)
                >>> stop_pitch = abjad.NumberedPitch(0)

            ::

                >>> start_pitch.interpolate(stop_pitch, abjad.Fraction(0))
                NumberedPitch(12)
                >>> start_pitch.interpolate(stop_pitch, abjad.Fraction(1, 4))
                NumberedPitch(9)
                >>> start_pitch.interpolate(stop_pitch, abjad.Fraction(1, 2))
                NumberedPitch(6)
                >>> start_pitch.interpolate(stop_pitch, abjad.Fraction(3, 4))
                NumberedPitch(3)
                >>> start_pitch.interpolate(stop_pitch, abjad.Fraction(1))
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

            Inverts pitch-class about pitch-class 0 explicitly:

            ::

                >>> abjad.NumberedPitch(2).invert(0)
                NumberedPitch(-2)

            ::

                >>> abjad.NumberedPitch(-2).invert(0)
                NumberedPitch(2)

        ..  container:: example

            Inverts pitch-class about pitch-class 0 implicitly:

            ::

                >>> abjad.NumberedPitch(2).invert()
                NumberedPitch(-2)

            ::

                >>> abjad.NumberedPitch(-2).invert()
                NumberedPitch(2)

        ..  container:: example

            Inverts pitch-class about pitch-class -3:

            ::

                >>> abjad.NumberedPitch(2).invert(-3)
                NumberedPitch(-8)

        Returns new numbered pitch.
        '''
        return Pitch.invert(self, axis=axis)

    def multiply(self, n=1):
        r'''Multiplies pitch by index `n`.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(14).multiply(3)
                NumberedPitch(42)

        Returns new numbered pitch.
        '''
        #pitch_class_number = (self.pitch_class_number * n) % 12
        #octave_floor = (self.octave.number - 4) * 12
        #return type(self)(pitch_class_number + octave_floor)
        return type(self)(n * self.number)

    def transpose(self, n=0):
        r'''Tranposes numbered pitch by `n` semitones.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).transpose(1)
                NumberedPitch(14)

        Returns new numbered pitch.
        '''
        semitones = self.pitch_number + float(n)
        return type(self)(semitones)
