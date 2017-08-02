# -*- coding: utf-8 -*-
import numbers
from abjad.tools import mathtools
from abjad.tools.pitchtools.Pitch import Pitch


class NumberedPitch(Pitch):
    r'''Numbered pitch.

    ::

        >>> import abjad

    ..  container:: example

        Initializes from number:

        ::

            >>> numbered_pitch = abjad.NumberedPitch(13)
            >>> show(numbered_pitch) # doctest: +SKIP

        ..  docs::

            >>> f(numbered_pitch.__illustrate__()[abjad.Staff])
            \new Staff \with {
                \override TimeSignature.stencil = ##f
            } {
                \clef "treble"
                cs''1 * 1/4
            }

    ..  container:: example

        Initializes from other numbered pitch

        ::

            >>> numbered_pitch = abjad.NumberedPitch(abjad.NumberedPitch(13))
            >>> show(numbered_pitch) # doctest: +SKIP

        ..  docs::

            >>> f(numbered_pitch.__illustrate__()[abjad.Staff])
            \new Staff \with {
                \override TimeSignature.stencil = ##f
            } {
                \clef "treble"
                cs''1 * 1/4
            }

    ..  container:: example

        Initializes from pitch-class / octave pair:

        ::

            >>> numbered_pitch = abjad.NumberedPitch((1, 5))
            >>> show(numbered_pitch) # doctest: +SKIP

        ..  docs::

            >>> f(numbered_pitch.__illustrate__()[abjad.Staff])
            \new Staff \with {
                \override TimeSignature.stencil = ##f
            } {
                \clef "treble"
                cs''1 * 1/4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    ### INITIALIZER ###

    def __init__(self, number=0, arrow=None):
        from abjad.tools import pitchtools
        try:
            number = number.number
        except AttributeError:
            pass
        if Pitch._is_pitch_number(number):
            number = number
        elif (isinstance(number, tuple) and
            len(number) == 2 and
            not isinstance(number[0], str)):
            pitch_class, octave = number
            pitch_class = getattr(pitch_class, 'number', pitch_class)
            assert isinstance(pitch_class, numbers.Number), repr(number)
            number = pitch_class + 12 * (octave - 4)
        else:
            if number is None:
                number = 0
            number = pitchtools.NamedPitch(number).number
        number = mathtools.integer_equivalent_number_to_integer(number)
        self._number = number
        if arrow not in (Up, Down, None):
            message = 'arrow must be up, down or none: {!r}.'
            message = message.format(arrow)
            raise TypeError(message)
        self._arrow = arrow

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        r'''Adds `argument` to numbered pitch.

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
        semitones = self.number + argument.number
        return type(self)(semitones)

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
                >>> pitch_1 < pitch_2
                False
                >>> pitch_1 < pitch_3
                True

            ::

                >>> pitch_2 < pitch_1
                False
                >>> pitch_2 < pitch_2
                False
                >>> pitch_2 < pitch_3
                True

            ::

                >>> pitch_3 < pitch_1
                False
                >>> pitch_3 < pitch_2
                False
                >>> pitch_3 < pitch_3
                False

        Returns true or false.
        '''
        try:
            argument = type(self)(argument)
        except (ValueError, TypeError):
            return False
        return self.number < argument.number

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
        return type(self)(-self.number)

    def __radd__(self, argument):
        r'''Adds numbered pitch to `argument`.

        ..  container:: example

            ::

                >>> pitch = abjad.NumberedPitch(13)
                >>> abjad.NumberedPitch(12).__radd__(pitch)
                NumberedPitch(25)

            ::

                >>> pitch = abjad.NumberedPitch(12)
                >>> abjad.NumberedPitch(13).__radd__(pitch)
                NumberedPitch(25)

        Returns new numbered pitch.
        '''
        argument = type(self)(argument)
        return argument.__add__(self)

    def __str__(self):
        r'''Gets string representation of numbered pitch.

        Returns string.
        '''
        return str(self.number)

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

    def _apply_accidental(self, accidental=None):
        from abjad.tools.pitchtools.Accidental import Accidental
        accidental = Accidental(accidental)
        semitones = self.number + accidental.semitones
        return type(self)(semitones)

    @staticmethod
    def _from_pitch_class_octave(pitch_class, octave):
        from abjad.tools import pitchtools
        pitch_class = pitchtools.NumberedPitchClass(pitch_class)
        octave = pitchtools.Octave(octave)
        number = 12 * (octave.number - 4) + pitch_class.number
        return NumberedPitch(number)

    def _get_diatonic_pitch_class_name(self):
        return self.pitch_class._get_diatonic_pitch_class_name()

    def _get_diatonic_pitch_class_number(self):
        return self.numbered_pitch_class._get_diatonic_pitch_class_number()

    def _get_diatonic_pitch_name(self):
        return '{}{}'.format(
            self._get_diatonic_pitch_class_name(),
            self.octave.ticks,
            )

    def _get_diatonic_pitch_number(self):
        result = 7 * (self.octave.number - 4)
        result += self._get_diatonic_pitch_class_number()
        return result

    def _get_format_specification(self):
        import abjad
        return abjad.FormatSpecification(
            client=self,
            coerce_for_equality=True,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=[self.number],
            storage_format_kwargs_names=['arrow'],
            )

    def _get_lilypond_format(self):
        return self.name

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        r'''Gets accidental of numbered pitch.

        ..  container:: example

            ::

                >>> abjad.NumberedPitchClass(13).accidental
                Accidental('sharp')

        Returns accidental.
        '''
        import abjad
        return abjad.NamedPitch(self.number).accidental

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
    def hertz(self):
        r'''Gets frequency of numbered pitch in Hertz.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(9).hertz
                440.0

            ::

                >>> abjad.NumberedPitch(0).hertz
                261.62...

            ::

                >>> abjad.NumberedPitch(12).hertz
                523.25...

        Returns float.
        '''
        return super(NumberedPitch, self).hertz

    @property
    def name(self):
        r'''Gets name of numbered pitch.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).name
                "cs''"

        Returns string
        '''
        return '{}{}'.format(
            self.pitch_class.name,
            self.octave.ticks,
            )

    @property
    def number(self):
        r'''Gets number of numbered pitch.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).number
                13

        Returns number.
        '''
        return self._number

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
        number = self._number // 12 + 4
        return pitchtools.Octave(number=number)

    @property
    def pitch_class(self):
        r'''Gets pitch-class of numbered pitch.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).pitch_class
                NumberedPitchClass(1)

        Returns numbered pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClass(self)

    ### PUBLIC METHODS ###

    @classmethod
    def from_hertz(class_, hertz):
        r'''Makes numbered pitch from `hertz`.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch.from_hertz(440)
                NumberedPitch(9)

            ::

                >>> abjad.NumberedPitch.from_hertz(519)
                NumberedPitch(0)

        Returns newly constructed numbered pitch.
        '''
        return super(NumberedPitch, class_).from_hertz(hertz)

    @classmethod
    def from_pitch_carrier(class_, pitch_carrier):
        r'''Makes numbered pitch from `pitch_carrier`.

        ..  container:: example

            Makes numbered pitch from named pitch:

            ::

                >>> pitch = abjad.NamedPitch(('df', 5))
                >>> abjad.NumberedPitch.from_pitch_carrier(pitch)
                NumberedPitch(13)

        ..  container:: example

            Makes numbered pitch from note:

            ::

                >>> note = abjad.Note("df''4")
                >>> abjad.NumberedPitch.from_pitch_carrier(note)
                NumberedPitch(13)

        ..  container:: example

            Makes numbered pitch from note-head:

            ::

                >>> note = abjad.Note("df''4")
                >>> abjad.NumberedPitch.from_pitch_carrier(note.note_head)
                NumberedPitch(13)

        ..  container:: example

            Makes numbered pitch from chord:

            ::

                >>> chord = abjad.Chord("<df''>4")
                >>> abjad.NumberedPitch.from_pitch_carrier(chord)
                NumberedPitch(13)

        ..  container:: example

            Makes numbered pitch from integer:

            ::

                >>> abjad.NumberedPitch.from_pitch_carrier(13)
                NumberedPitch(13)

        ..  container:: example

            Makes numbered pitch from numbered pitch-class:

            ::

                >>> pitch_class = abjad.NumberedPitchClass(13)
                >>> abjad.NumberedPitch.from_pitch_carrier(pitch_class)
                NumberedPitch(1)

        Raises value error when `pitch_carrier` carries no pitch.

        Raises value error when `pitch_carrier` carries more than one pitch.

        Returns new numbered pitch.
        '''
        return super(NumberedPitch, class_).from_pitch_carrier(pitch_carrier)

    def get_name(self, locale=None):
        r'''Gets name of numbered pitch name according to `locale`.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).get_name()
                "cs''"

            ::

                >>> abjad.NumberedPitch(13).get_name(locale='us')
                'C#5'

        Set `locale` to `'us'` or none.

        Returns string.
        '''
        import abjad
        return abjad.NamedPitch(self).get_name(locale=locale)

    def interpolate(self, stop_pitch, fraction):
        r'''Interpolates between numbered pitch and `stop_pitch` by `fraction`.

        ..  container:: example

            Interpolates from C4 to C5:

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

            Interpolates from C5 to C4:

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

        Returns new numbered pitch.
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
        pitch_number = self.number
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
        r'''Inverts numbered pitch around `axis`.

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
        r'''Multiplies numbered pitch by index `n`.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(14).multiply(3)
                NumberedPitch(42)

        Returns new numbered pitch.
        '''
        return super(NumberedPitch, self).multiply(n=n)

    def transpose(self, n=0):
        r'''Tranposes numbered pitch by `n` semitones.

        ..  container:: example

            ::

                >>> abjad.NumberedPitch(13).transpose(1)
                NumberedPitch(14)

        Returns new numbered pitch.
        '''
        import abjad
        interval = abjad.NumberedInterval(n)
        return interval.transpose(self)
