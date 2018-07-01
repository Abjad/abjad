from abjad import mathtools
from abjad.system.FormatSpecification import FormatSpecification
from . import constants
from .Pitch import Pitch


class NumberedPitch(Pitch):
    r"""
    Numbered pitch.

    ..  container:: example

        Initializes from number:

        >>> numbered_pitch = abjad.NumberedPitch(13)
        >>> abjad.show(numbered_pitch) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(numbered_pitch.__illustrate__()[abjad.Staff])
            \new Staff
            \with
            {
                \override TimeSignature.stencil = ##f
            }
            {
                \clef "treble"
                cs''1 * 1/4
            }

    ..  container:: example

        Initializes from other numbered pitch

        >>> numbered_pitch = abjad.NumberedPitch(abjad.NumberedPitch(13))
        >>> abjad.show(numbered_pitch) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(numbered_pitch.__illustrate__()[abjad.Staff])
            \new Staff
            \with
            {
                \override TimeSignature.stencil = ##f
            }
            {
                \clef "treble"
                cs''1 * 1/4
            }

    ..  container:: example

        Initializes from pitch-class / octave pair:

        >>> numbered_pitch = abjad.NumberedPitch((1, 5))
        >>> abjad.show(numbered_pitch) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(numbered_pitch.__illustrate__()[abjad.Staff])
            \new Staff
            \with
            {
                \override TimeSignature.stencil = ##f
            }
            {
                \clef "treble"
                cs''1 * 1/4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        number=0, *,
        arrow=None,
        octave=None,
    ):
        super().__init__(
            number or 0,
            arrow=arrow,
            octave=octave,
            )

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        """
        Adds `argument` to numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(12) + abjad.NumberedPitch(13)
            NumberedPitch(25)

            >>> abjad.NumberedPitch(13) + abjad.NumberedPitch(12)
            NumberedPitch(25)

        Returns new numbered pitch.
        """
        argument = type(self)(argument)
        semitones = float(self) + float(argument)
        return type(self)(semitones)

    def __lt__(self, argument):
        r"""Is true when `argument` can be coerced to a numbered pitch and when this
        numbered pitch is less than `argument`.

        ..  container:: example

            >>> pitch_1 = abjad.NumberedPitch(12)
            >>> pitch_2 = abjad.NumberedPitch(12)
            >>> pitch_3 = abjad.NumberedPitch(13)

            >>> pitch_1 < pitch_1
            False
            >>> pitch_1 < pitch_2
            False
            >>> pitch_1 < pitch_3
            True

            >>> pitch_2 < pitch_1
            False
            >>> pitch_2 < pitch_2
            False
            >>> pitch_2 < pitch_3
            True

            >>> pitch_3 < pitch_1
            False
            >>> pitch_3 < pitch_2
            False
            >>> pitch_3 < pitch_3
            False

        Returns true or false.
        """
        try:
            argument = type(self)(argument)
        except (ValueError, TypeError):
            return False
        return self.number < argument.number

    def __neg__(self):
        """
        Negates numbered pitch.

        ..  container:: example

            >>> -abjad.NumberedPitch(13.5)
            NumberedPitch(-13.5)

            >>> -abjad.NumberedPitch(-13.5)
            NumberedPitch(13.5)

        Returns new numbered pitch.
        """
        return type(self)(-self.number)

    def __radd__(self, argument):
        """
        Adds numbered pitch to `argument`.

        ..  container:: example

            >>> pitch = abjad.NumberedPitch(13)
            >>> abjad.NumberedPitch(12).__radd__(pitch)
            NumberedPitch(25)

            >>> pitch = abjad.NumberedPitch(12)
            >>> abjad.NumberedPitch(13).__radd__(pitch)
            NumberedPitch(25)

        Returns new numbered pitch.
        """
        argument = type(self)(argument)
        return argument.__add__(self)

    def __str__(self):
        """
        Gets string representation of numbered pitch.

        Returns string.
        """
        return str(self.number)

    def __sub__(self, argument):
        """
        Subtracts `argument` from numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(12) - abjad.NumberedPitch(12)
            NumberedInterval(0)

            >>> abjad.NumberedPitch(12) - abjad.NumberedPitch(13)
            NumberedInterval(1)

            >>> abjad.NumberedPitch(13) - abjad.NumberedPitch(12)
            NumberedInterval(-1)

        Returns numbered interval.
        """
        import abjad
        if isinstance(argument, type(self)):
            return abjad.NumberedInterval.from_pitch_carriers(
                self, argument)
        interval = abjad.NumberedInterval(argument)
        interval = -interval
        return interval.transpose(self)

    ### PRIVATE METHODS ###

    def _apply_accidental(self, accidental=None):
        import abjad
        accidental = abjad.Accidental(accidental)
        semitones = self.number + accidental.semitones
        return type(self)(semitones)

    def _from_named_parts(self, dpc_number, alteration, octave):
        import abjad
        pc_number = constants._diatonic_pc_number_to_pitch_class_number[dpc_number]
        pc_number += alteration
        pc_number += (octave - 4) * 12
        self._number = mathtools.integer_equivalent_number_to_integer(pc_number)
        octave_number, pc_number = divmod(self._number, 12)
        self._pitch_class = abjad.NumberedPitchClass(pc_number)
        self._octave = abjad.Octave(octave_number + 4)

    def _from_number(self, number):
        import abjad
        self._number = self._to_nearest_quarter_tone(number)
        octave_number, pc_number = divmod(self._number, 12)
        self._octave = abjad.Octave(octave_number + 4)
        self._pitch_class = abjad.NumberedPitchClass(pc_number)

    def _from_pitch_or_pitch_class(self, pitch_or_pitch_class):
        import abjad
        self._number = self._to_nearest_quarter_tone(float(pitch_or_pitch_class))
        octave_number, pc_number = divmod(self._number, 12)
        self._octave = abjad.Octave(octave_number + 4)
        self._pitch_class = abjad.NumberedPitchClass(
            pc_number,
            arrow=pitch_or_pitch_class.arrow,
            )

    def _get_diatonic_pc_name(self):
        return self.pitch_class._get_diatonic_pc_name()

    def _get_diatonic_pc_number(self):
        return self.numbered_pitch_class._get_diatonic_pc_number()

    def _get_diatonic_pitch_number(self):
        result = 7 * (self.octave.number - 4)
        result += self._get_diatonic_pc_number()
        return result

    def _get_format_specification(self):
        return FormatSpecification(
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
        """
        Gets accidental of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitchClass(13).accidental
            Accidental('sharp')

        Returns accidental.
        """
        return self.pitch_class.accidental

    @property
    def arrow(self):
        """
        Gets arrow of numbered pitch.

        ..  container:: example

            Gets no arrow:

            >>> abjad.NumberedPitch(13).arrow is None
            True

        ..  container:: example

            Gets up-arrow:

            >>> abjad.NumberedPitch(13, arrow=abjad.Up).arrow
            Up

        ..  container:: example

            Gets down-arrow:

            >>> abjad.NumberedPitch(13, arrow=abjad.Down).arrow
            Down

        Returns up, down or none.
        """
        return self._pitch_class.arrow

    @property
    def hertz(self):
        """
        Gets frequency of numbered pitch in Hertz.

        ..  container:: example

            >>> abjad.NumberedPitch(9).hertz
            440.0

            >>> abjad.NumberedPitch(0).hertz
            261.62...

            >>> abjad.NumberedPitch(12).hertz
            523.25...

        Returns float.
        """
        return super().hertz

    @property
    def name(self):
        """
        Gets name of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(13).name
            "cs''"

        Returns string
        """
        return '{}{}'.format(
            self.pitch_class.name,
            self.octave.ticks,
            )

    @property
    def number(self):
        """
        Gets number of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(13).number
            13

        Returns number.
        """
        pc_number = float(self.pitch_class)
        octave_base_pitch = (self.octave.number - 4) * 12
        return mathtools.integer_equivalent_number_to_integer(
            pc_number + octave_base_pitch
            )

    @property
    def octave(self):
        """
        Gets octave of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(13).octave
            Octave(5)

        Returns octave.
        """
        return self._octave

    @property
    def pitch_class(self):
        """
        Gets pitch-class of numbered pitch.

        ..  container:: example

            >>> abjad.NumberedPitch(13).pitch_class
            NumberedPitchClass(1)

        Returns numbered pitch-class.
        """
        return self._pitch_class

    ### PUBLIC METHODS ###

    @classmethod
    def from_hertz(class_, hertz):
        """
        Makes numbered pitch from `hertz`.

        ..  container:: example

            >>> abjad.NumberedPitch.from_hertz(440)
            NumberedPitch(9)

        ..  container:: example

            REGRESSION. Returns 12 (not 0):

            >>> abjad.NumberedPitch.from_hertz(519)
            NumberedPitch(12)

        Returns newly constructed numbered pitch.
        """
        return super().from_hertz(hertz)

    def get_name(self, locale=None):
        """
        Gets name of numbered pitch name according to `locale`.

        ..  container:: example

            >>> abjad.NumberedPitch(13).get_name()
            "cs''"

            >>> abjad.NumberedPitch(13).get_name(locale='us')
            'C#5'

        Set `locale` to `'us'` or none.

        Returns string.
        """
        import abjad
        return abjad.NamedPitch(self).get_name(locale=locale)

    def interpolate(self, stop_pitch, fraction):
        """
        Interpolates between numbered pitch and `stop_pitch` by `fraction`.

        ..  container:: example

            Interpolates from C4 to C5:

            >>> start_pitch = abjad.NumberedPitch(0)
            >>> stop_pitch = abjad.NumberedPitch(12)

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

            >>> start_pitch = abjad.NumberedPitch(12)
            >>> stop_pitch = abjad.NumberedPitch(0)

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
        """
        import abjad
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
        pitch = abjad.NumberedPitch(pitch_number)
        if self <= stop_pitch:
            triple = (self, pitch, stop_pitch)
            assert self <= pitch <= stop_pitch, triple
        else:
            triple = (self, pitch, stop_pitch)
            assert self >= pitch >= stop_pitch, triple
        return pitch

    def invert(self, axis=None):
        """
        Inverts numbered pitch around `axis`.

        ..  container:: example

            Inverts pitch-class about pitch-class 0 explicitly:

            >>> abjad.NumberedPitch(2).invert(0)
            NumberedPitch(-2)

            >>> abjad.NumberedPitch(-2).invert(0)
            NumberedPitch(2)

        ..  container:: example

            Inverts pitch-class about pitch-class 0 implicitly:

            >>> abjad.NumberedPitch(2).invert()
            NumberedPitch(-2)

            >>> abjad.NumberedPitch(-2).invert()
            NumberedPitch(2)

        ..  container:: example

            Inverts pitch-class about pitch-class -3:

            >>> abjad.NumberedPitch(2).invert(-3)
            NumberedPitch(-8)

        Returns new numbered pitch.
        """
        return Pitch.invert(self, axis=axis)

    def multiply(self, n=1):
        """
        Multiplies numbered pitch by index `n`.

        ..  container:: example

            >>> abjad.NumberedPitch(14).multiply(3)
            NumberedPitch(42)

        Returns new numbered pitch.
        """
        return super().multiply(n=n)

    def transpose(self, n=0):
        """
        Tranposes numbered pitch by `n` semitones.

        ..  container:: example

            >>> abjad.NumberedPitch(13).transpose(1)
            NumberedPitch(14)

        Returns new numbered pitch.
        """
        import abjad
        interval = abjad.NumberedInterval(n)
        return type(self)(float(self) + float(interval))
