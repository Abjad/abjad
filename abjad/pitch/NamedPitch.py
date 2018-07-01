import math
from abjad import mathtools
from . import constants
from abjad.system.FormatSpecification import FormatSpecification
from .Pitch import Pitch


class NamedPitch(Pitch):
    r"""
    Named pitch.

    ..  container:: example

        Initializes from pitch name:

        >>> pitch = abjad.NamedPitch("cs''")
        >>> abjad.show(pitch) # doctest: +SKIP

        ..  docs::

            >>> staff = pitch.__illustrate__()[abjad.Staff]
            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TimeSignature.stencil = ##f
            }
            {
                \clef "treble"
                cs''1 * 1/4
            }

        Initializes quartertone from pitch name:

        >>> pitch = abjad.NamedPitch("aqs")
        >>> abjad.show(pitch) # doctest: +SKIP

        ..  docs::

            >>> staff = pitch.__illustrate__()[abjad.Staff]
            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TimeSignature.stencil = ##f
            }
            {
                \clef "bass"
                aqs1 * 1/4
            }

    ..  container:: example

        Initializes from pitch-class / octave string:

        >>> pitch = abjad.NamedPitch('C#5')
        >>> abjad.show(pitch) # doctest: +SKIP

        ..  docs::

            >>> staff = pitch.__illustrate__()[abjad.Staff]
            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TimeSignature.stencil = ##f
            }
            {
                \clef "treble"
                cs''1 * 1/4
            }

        Initializes quartertone from pitch-class / octave string:

        >>> pitch = abjad.NamedPitch('A+3')
        >>> abjad.show(pitch) # doctest: +SKIP

        ..  docs::

            >>> staff = pitch.__illustrate__()[abjad.Staff]
            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TimeSignature.stencil = ##f
            }
            {
                \clef "bass"
                aqs1 * 1/4
            }

        >>> pitch = abjad.NamedPitch('Aqs3')
        >>> abjad.show(pitch) # doctest: +SKIP

        ..  docs::

            >>> staff = pitch.__illustrate__()[abjad.Staff]
            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TimeSignature.stencil = ##f
            }
            {
                \clef "bass"
                aqs1 * 1/4
            }

    ..  container:: example

        Initializes arrowed pitch:

        >>> pitch = abjad.NamedPitch('C#5', arrow=abjad.Up)
        >>> abjad.show(pitch) # doctest: +SKIP

        ..  docs::

            >>> staff = pitch.__illustrate__()[abjad.Staff]
            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TimeSignature.stencil = ##f
            }
            {
                \once \override Accidental.stencil = #ly:text-interface::print
                \once \override Accidental.text = \markup { \musicglyph #"accidentals.sharp.arrowup" }
                \clef "treble"
                cs''1 * 1/4
            }

    ..  container:: example

        REGRESSION. Small floats just less than a C initialize in the correct
        octave.

        Initializes c / C3:

        >>> pitch = abjad.NamedPitch(-12.1)
        >>> abjad.show(pitch) # doctest: +SKIP

        ..  docs::

            >>> staff = pitch.__illustrate__()[abjad.Staff]
            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TimeSignature.stencil = ##f
            }
            {
                \clef "bass"
                c1 * 1/4
            }

        Initializes c' / C4:

        >>> pitch = abjad.NamedPitch(-0.1)
        >>> abjad.show(pitch) # doctest: +SKIP

        ..  docs::

            >>> staff = pitch.__illustrate__()[abjad.Staff]
            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TimeSignature.stencil = ##f
            }
            {
                \clef "treble"
                c'1 * 1/4
            }

        Initializes c'' / C5:

        >>> pitch = abjad.NamedPitch(11.9)
        >>> abjad.show(pitch) # doctest: +SKIP

        ..  docs::

            >>> staff = pitch.__illustrate__()[abjad.Staff]
            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TimeSignature.stencil = ##f
            }
            {
                \clef "treble"
                c''1 * 1/4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        name="c'",
        *,
        accidental=None,
        arrow=None,
        octave=None,
    ):
        super().__init__(
            name or "c'",
            accidental=accidental,
            arrow=arrow,
            octave=octave,
            )

    ### SPECIAL METHODS ###

    def __add__(self, interval):
        """
        Adds named pitch to `interval`.

        ..  container:: example

            >>> abjad.NamedPitch("cs''") + abjad.NamedInterval('-M2')
            NamedPitch("b'")

            >>> abjad.NamedPitch("cs''") + abjad.NamedInterval('P1')
            NamedPitch("cs''")

            >>> abjad.NamedPitch("cs''") + abjad.NamedInterval('+M2')
            NamedPitch("ds''")

        Returns new named pitch.
        """
        import abjad
        interval = abjad.NamedInterval(interval)
        return interval.transpose(self)

    def __copy__(self, *arguments):
        """
        Copies named pitch.

        >>> import copy

        ..  container:: example

            >>> copy.copy(abjad.NamedPitch("c''"))
            NamedPitch("c''")

            >>> copy.copy(abjad.NamedPitch("cs''"))
            NamedPitch("cs''")

            >>> copy.copy(abjad.NamedPitch("df''"))
            NamedPitch("df''")

        ..  container:: example

            Copies arrowed pitch:

            >>> pitch = abjad.NamedPitch("cs''", arrow=abjad.Up)
            >>> copy.copy(pitch)
            NamedPitch("cs''", arrow=Up)

        Returns new named pitch.
        """
        return type(self)(self, arrow=self.arrow)

    def __eq__(self, argument):
        """
        Is true when `argument` is a named pitch equal to this named pitch.

        ..  container:: example

            >>> pitch_1 = abjad.NamedPitch('fs')
            >>> pitch_2 = abjad.NamedPitch('fs')
            >>> pitch_3 = abjad.NamedPitch('gf')

            >>> pitch_1 == pitch_1
            True
            >>> pitch_1 == pitch_2
            True
            >>> pitch_1 == pitch_3
            False

            >>> pitch_2 == pitch_1
            True
            >>> pitch_2 == pitch_2
            True
            >>> pitch_2 == pitch_3
            False

            >>> pitch_3 == pitch_1
            False
            >>> pitch_3 == pitch_2
            False
            >>> pitch_3 == pitch_3
            True

        Returns true or false.
        """
        return super().__eq__(argument)

    def __hash__(self):
        """
        Hashes named pitch.

        Returns integer.
        """
        return super().__hash__()

    def __lt__(self, argument):
        """
        Is true when named pitch is less than `argument`.

        ..  container:: example

            >>> pitch_1 = abjad.NamedPitch('fs')
            >>> pitch_2 = abjad.NamedPitch('fs')
            >>> pitch_3 = abjad.NamedPitch('gf')

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
        except (TypeError, ValueError):
            return False
        self_dpn = self._get_diatonic_pitch_number()
        argument_dpn = argument._get_diatonic_pitch_number()
        if self_dpn == argument_dpn:
            return self.accidental < argument.accidental
        return self_dpn < argument_dpn

    def __radd__(self, interval):
        """
        Right-addition not defined on named pitches.

        ..  container:: example

            >>> abjad.NamedPitch("cs'").__radd__(1)
            Traceback (most recent call last):
                ...
            NotImplementedError: right-addition not defined on NamedPitch.

        """
        message = 'right-addition not defined on {}.'
        message = message.format(type(self).__name__)
        raise NotImplementedError(message)

    def __str__(self):
        """
        Gets string representation of named pitch.

        ..  container:: example

            >>> str(abjad.NamedPitch("c''"))
            "c''"

            >>> str(abjad.NamedPitch("cs''"))
            "cs''"

            >>> str(abjad.NamedPitch("df''"))
            "df''"

        Returns string.
        """
        return self.name

    def __sub__(self, argument):
        """
        Subtracts `argument` from named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("cs''") - abjad.NamedPitch("b'")
            NamedInterval('-M2')

            >>> abjad.NamedPitch("cs''") - abjad.NamedPitch("fs''")
            NamedInterval('+P4')

        Returns named interval.
        """
        import abjad
        if isinstance(argument, type(self)):
            return abjad.NamedInterval.from_pitch_carriers(self, argument)
        interval = abjad.NamedInterval(argument)
        interval = -interval
        return interval.transpose(self)

    ### PRIVATE METHODS ###

    def _apply_accidental(self, accidental):
        import abjad
        name = self._get_diatonic_pc_name()
        name += str(self.accidental + abjad.Accidental(accidental))
        name += self.octave.ticks
        return type(self)(name)

    def _from_named_parts(self, dpc_number, alteration, octave):
        import abjad
        dpc_name = constants._diatonic_pc_number_to_diatonic_pc_name[dpc_number]
        accidental = abjad.Accidental(alteration)
        octave = abjad.Octave(octave)
        self._octave = octave
        self._pitch_class = abjad.NamedPitchClass(dpc_name + str(accidental))

    def _from_number(self, number):
        import abjad
        number = self._to_nearest_quarter_tone(number)
        div, mod = divmod(number, 12)
        pitch_class = abjad.NumberedPitchClass(mod)
        self._from_named_parts(
            dpc_number=pitch_class._get_diatonic_pc_number(),
            alteration=pitch_class._get_alteration(),
            octave=div + 4,
            )

    def _from_pitch_or_pitch_class(self, pitch_or_pitch_class):
        import abjad
        name = format(pitch_or_pitch_class, 'lilypond')
        if not isinstance(pitch_or_pitch_class, Pitch):
            name += "'"
        if isinstance(pitch_or_pitch_class, Pitch):
            self._pitch_class = abjad.NamedPitchClass(
                pitch_or_pitch_class.pitch_class,
                )
            self._octave = pitch_or_pitch_class.octave
        else:
            self._pitch_class = abjad.NamedPitchClass(
                pitch_or_pitch_class,
                )
            self._octave = abjad.Octave()

    def _get_alteration(self):
        return self.accidental.semitones

    def _get_diatonic_pc_name(self):
        return constants._diatonic_pc_number_to_diatonic_pc_name[
            self.pitch_class._diatonic_pc_number]

    def _get_diatonic_pc_number(self):
        diatonic_pc_name = self._get_diatonic_pc_name()
        diatonic_pc_number = (
            constants._diatonic_pc_name_to_diatonic_pc_number[
                diatonic_pc_name]
            )
        return diatonic_pc_number

    def _get_diatonic_pitch_number(self):
        diatonic_pitch_number = 7 * (self.octave.number - 4)
        diatonic_pitch_number += self._get_diatonic_pc_number()
        return diatonic_pitch_number

    def _get_format_specification(self):
        return FormatSpecification(
            self,
            coerce_for_equality=True,
            repr_is_indented=False,
            storage_format_args_values=[self.name],
            storage_format_is_indented=False,
            storage_format_kwargs_names=['arrow'],
            )

    def _get_lilypond_format(self):
        return str(self)

    def _list_format_contributions(self):
        contributions = []
        if self.arrow is None:
            return contributions
        string = r'\once \override Accidental.stencil ='
        string += ' #ly:text-interface::print'
        contributions.append(string)
        glyph = f'accidentals.{self.accidental.name}'
        glyph += f'.arrow{str(self.arrow).lower()}'
        string = r'\once \override Accidental.text ='
        string += rf' \markup {{ \musicglyph #"{glyph}" }}'
        contributions.append(string)
        return contributions

    def _respell_with_flats(self):
        name = constants._pitch_class_number_to_pitch_class_name_with_flats[
            self.pitch_class.number
            ]
        pitch = type(self)((name, self.octave.number))
        return pitch

    def _respell_with_sharps(self):
        name = constants._pitch_class_number_to_pitch_class_name_with_sharps[
            self.pitch_class.number
            ]
        pitch = type(self)((name, self.octave.number))
        return pitch

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        """
        Gets accidental of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").accidental
            Accidental('natural')

            >>> abjad.NamedPitch("cs''").accidental
            Accidental('sharp')

            >>> abjad.NamedPitch("df''").accidental
            Accidental('flat')

        Returns accidental.
        """
        return self.pitch_class.accidental

    @property
    def arrow(self):
        """
        Gets arrow of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("cs''").arrow is None
            True

            >>> abjad.NamedPitch("cs''", arrow=abjad.Up).arrow
            Up

            >>> abjad.NamedPitch("cs''", arrow=abjad.Down).arrow
            Down

        ..  container:: example

            Displays arrow in interpreter representation:

            >>> abjad.NamedPitch("cs''", arrow=abjad.Down)
            NamedPitch("cs''", arrow=Down)

        Returns up, down or none.
        """
        return self._pitch_class.arrow

    @property
    def hertz(self):
        """
        Gets frequency of named pitch in Hertz.

        ..  container:: example

            >>> abjad.NamedPitch("c''").hertz
            523.25...

            >>> abjad.NamedPitch("cs''").hertz
            554.36...

            >>> abjad.NamedPitch("df''").hertz
            554.36...

        Returns float.
        """
        return super().hertz

    @property
    def name(self):
        """
        Gets name of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").name
            "c''"

            >>> abjad.NamedPitch("cs''").name
            "cs''"

            >>> abjad.NamedPitch("df''").name
            "df''"

        Returns string.
        """
        return '{!s}{!s}'.format(
            self.pitch_class,
            self.octave,
            )

    @property
    def number(self):
        """
        Gets number of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").number
            12

            >>> abjad.NamedPitch("cs''").number
            13

            >>> abjad.NamedPitch("df''").number
            13

            >>> abjad.NamedPitch("cf'").number
            -1

        Returns number.
        """
        diatonic_pc_number = self.pitch_class._get_diatonic_pc_number()
        pc_number = constants._diatonic_pc_number_to_pitch_class_number[diatonic_pc_number]
        alteration = self.pitch_class._get_alteration()
        octave_base_pitch = (self.octave.number - 4) * 12
        return mathtools.integer_equivalent_number_to_integer(
            pc_number + alteration + octave_base_pitch
            )

    @property
    def octave(self):
        """
        Gets octave of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").octave
            Octave(5)

            >>> abjad.NamedPitch("cs''").octave
            Octave(5)

            >>> abjad.NamedPitch("df''").octave
            Octave(5)

        Returns octave.
        """
        return self._octave

    @property
    def pitch_class(self):
        """
        Gets pitch-class of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").pitch_class
            NamedPitchClass('c')

            >>> abjad.NamedPitch("cs''").pitch_class
            NamedPitchClass('cs')

            >>> abjad.NamedPitch("df''").pitch_class
            NamedPitchClass('df')

        Returns named pitch-class.
        """
        return self._pitch_class

    ### PUBLIC METHODS ###

    @classmethod
    def from_hertz(class_, hertz):
        """
        Makes named pitch from `hertz`.

        ..  container:: example

            >>> abjad.NamedPitch.from_hertz(440)
            NamedPitch("a'")

        ..  container:: example

            REGRESSION. Returns c'' (C5) and not c' (C4):

            >>> abjad.NamedPitch.from_hertz(519)
            NamedPitch("c''")

        Returns newly constructed named pitch.
        """
        return super().from_hertz(hertz)

    def get_name(self, locale=None):
        """
        Gets name of named pitch according to `locale`.

        ..  container:: example

            >>> abjad.NamedPitch("cs''").get_name()
            "cs''"

            >>> abjad.NamedPitch("cs''").get_name(locale='us')
            'C#5'

        Set `locale` to `'us'` or none.

        Returns string.
        """
        if locale is None:
            return self.name
        elif locale == 'us':
            return '{}{}{}'.format(
                self._get_diatonic_pc_name().upper(),
                self.accidental.symbol,
                self.octave.number,
                )
        else:
            message = "must be 'us' or none: {!r}."
            message = message.format(locale)
            raise ValueError(message)

    def invert(self, axis=None):
        """
        Inverts named pitch around `axis`.

        ..  container:: example

            Inverts pitch around middle C explicitly:

            >>> abjad.NamedPitch("d'").invert("c'")
            NamedPitch('bf')

            >>> abjad.NamedPitch('bf').invert("c'")
            NamedPitch("d'")

        ..  container:: example

            Inverts pitch around middle C implicitly:

            >>> abjad.NamedPitch("d'").invert()
            NamedPitch('bf')

            >>> abjad.NamedPitch('bf').invert()
            NamedPitch("d'")

        ..  container:: example

            Inverts pitch around A3:

            >>> abjad.NamedPitch("d'").invert('a')
            NamedPitch('e')

        Interprets none-valued `axis` equal to middle C.

        Returns new named pitch.
        """
        return super().invert(axis=axis)

    def multiply(self, n=1):
        """
        Multiplies named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("d'").multiply(1)
            NamedPitch("d'")

            >>> abjad.NamedPitch("d'").multiply(3)
            NamedPitch("fs'")

            >>> abjad.NamedPitch("d'").multiply(6)
            NamedPitch("c''")

            >>> abjad.NamedPitch("d'").multiply(6.5)
            NamedPitch("cs''")

        Returns new named pitch.
        """
        return super().multiply(n=n)

    def simplify(self):
        """
        Reduce alteration to between -2 and 2 while maintaining identical pitch
        number.

            >>> abjad.NamedPitch("cssqs'").simplify()
            NamedPitch("dqs'")

            >>> abjad.NamedPitch("cfffqf'").simplify()
            NamedPitch('aqf')

            >>> float(abjad.NamedPitch("cfffqf'").simplify()) == float(NamedPitch('aqf'))
            True

        ..  note:: LilyPond by default only supports accidentals from
                   double-flat to double-sharp.

        Returns named pitch.
        """
        import abjad
        alteration = self._get_alteration()
        if abs(alteration) <= 2:
            return self
        diatonic_pc_number = self._get_diatonic_pc_number()
        octave = int(self.octave)
        while alteration > 2:
            step_size = 2
            if diatonic_pc_number == 2:  # e to f
                step_size = 1
            elif diatonic_pc_number == 6:  # b to c
                step_size = 1
                octave += 1
            diatonic_pc_number = (diatonic_pc_number + 1) % 7
            alteration -= step_size
        while alteration < -2:
            step_size = 2
            if diatonic_pc_number == 3:  # f to e
                step_size = 1
            elif diatonic_pc_number == 0:  # c to b
                step_size = 1
                octave -= 1
            diatonic_pc_number = (diatonic_pc_number - 1) % 7
            alteration += step_size
        diatonic_pc_name = constants._diatonic_pc_number_to_diatonic_pc_name[
            diatonic_pc_number]
        accidental = abjad.Accidental(alteration)
        octave = abjad.Octave(octave)
        pitch_name = '{}{!s}{!s}'.format(diatonic_pc_name, accidental, octave)
        return type(self)(pitch_name, arrow=self.arrow)

    # TODO: duplicate on NumberedPitch
    def to_staff_position(self, clef=None):
        r"""
        Changes named pitch to staff position.

        ..  container:: example

            Changes C#5 to absolute staff position:

            >>> abjad.NamedPitch('C#5').to_staff_position()
            StaffPosition(7)

            >>> abjad.NamedPitch('C#5').to_staff_position(clef='treble')
            StaffPosition(1)

            >>> abjad.NamedPitch('C#5').to_staff_position(clef='bass')
            StaffPosition(13)

        ..  container:: example

            Marks up absolute staff position of many pitches:

            >>> staff = abjad.Staff("g16 a b c' d' e' f' g' a' b' c'' d'' e'' f'' g'' a''")
            >>> for note in staff:
            ...     staff_position = note.written_pitch.to_staff_position()
            ...     markup = abjad.Markup(staff_position.number)
            ...     abjad.attach(markup, note)
            ...
            >>> abjad.override(staff).text_script.staff_padding = 5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = #5
                }
                {
                    g16
                    - \markup { -3 }
                    a16
                    - \markup { -2 }
                    b16
                    - \markup { -1 }
                    c'16
                    - \markup { 0 }
                    d'16
                    - \markup { 1 }
                    e'16
                    - \markup { 2 }
                    f'16
                    - \markup { 3 }
                    g'16
                    - \markup { 4 }
                    a'16
                    - \markup { 5 }
                    b'16
                    - \markup { 6 }
                    c''16
                    - \markup { 7 }
                    d''16
                    - \markup { 8 }
                    e''16
                    - \markup { 9 }
                    f''16
                    - \markup { 10 }
                    g''16
                    - \markup { 11 }
                    a''16
                    - \markup { 12 }
                }

        ..  container:: example

            Marks up treble staff position of many pitches:

            >>> staff = abjad.Staff("g16 a b c' d' e' f' g' a' b' c'' d'' e'' f'' g'' a''")
            >>> clef = abjad.Clef('treble')
            >>> for note in staff:
            ...     staff_position = note.written_pitch.to_staff_position(
            ...         clef=clef
            ...         )
            ...     markup = abjad.Markup(staff_position.number)
            ...     abjad.attach(markup, note)
            ...
            >>> abjad.override(staff).text_script.staff_padding = 5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = #5
                }
                {
                    g16
                    - \markup { -9 }
                    a16
                    - \markup { -8 }
                    b16
                    - \markup { -7 }
                    c'16
                    - \markup { -6 }
                    d'16
                    - \markup { -5 }
                    e'16
                    - \markup { -4 }
                    f'16
                    - \markup { -3 }
                    g'16
                    - \markup { -2 }
                    a'16
                    - \markup { -1 }
                    b'16
                    - \markup { 0 }
                    c''16
                    - \markup { 1 }
                    d''16
                    - \markup { 2 }
                    e''16
                    - \markup { 3 }
                    f''16
                    - \markup { 4 }
                    g''16
                    - \markup { 5 }
                    a''16
                    - \markup { 6 }
                }

        ..  container:: example

            Marks up bass staff position of many pitches:

            >>> staff = abjad.Staff("g,16 a, b, c d e f g a b c' d' e' f' g' a'")
            >>> clef = abjad.Clef('bass')
            >>> abjad.attach(clef, staff[0])
            >>> for note in staff:
            ...     staff_position = note.written_pitch.to_staff_position(
            ...         clef=clef
            ...         )
            ...     markup = abjad.Markup(staff_position.number)
            ...     abjad.attach(markup, note)
            ...
            >>> abjad.override(staff).text_script.staff_padding = 5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = #5
                }
                {
                    \clef "bass"
                    g,16
                    - \markup { -4 }
                    a,16
                    - \markup { -3 }
                    b,16
                    - \markup { -2 }
                    c16
                    - \markup { -1 }
                    d16
                    - \markup { 0 }
                    e16
                    - \markup { 1 }
                    f16
                    - \markup { 2 }
                    g16
                    - \markup { 3 }
                    a16
                    - \markup { 4 }
                    b16
                    - \markup { 5 }
                    c'16
                    - \markup { 6 }
                    d'16
                    - \markup { 7 }
                    e'16
                    - \markup { 8 }
                    f'16
                    - \markup { 9 }
                    g'16
                    - \markup { 10 }
                    a'16
                    - \markup { 11 }
                }

        Returns staff position.
        """
        import abjad
        staff_position_number = self._get_diatonic_pitch_number()
        if clef is not None:
            clef = abjad.Clef(clef)
            staff_position_number += clef.middle_c_position.number
        staff_position = abjad.StaffPosition(staff_position_number)
        return staff_position

    def transpose(self, n=0):
        """
        Transposes named pitch by index `n`.

        ..  container:: example

            Transposes C4 up a minor second:

            >>> abjad.NamedPitch("c'").transpose(n='m2')
            NamedPitch("df'")

        ..  container:: example

            Transposes C4 down a major second:

            >>> abjad.NamedPitch("c'").transpose(n='-M2')
            NamedPitch('bf')

        Returns new named pitch.
        """
        import abjad
        interval = abjad.NamedInterval(n)
        pitch_number = self.number + interval.semitones
        diatonic_pc_number = self._get_diatonic_pc_number()
        diatonic_pc_number += interval.staff_spaces
        diatonic_pc_number %= 7
        diatonic_pc_name = \
            constants._diatonic_pc_number_to_diatonic_pc_name[
                diatonic_pc_number]
        pc = constants._diatonic_pc_name_to_pitch_class_number[
            diatonic_pc_name
            ]
        nearest_neighbor = self._to_nearest_octave(pitch_number, pc)
        semitones = pitch_number - nearest_neighbor
        accidental = abjad.Accidental(semitones)
        octave = int(math.floor((pitch_number - semitones) / 12)) + 4
        octave = abjad.Octave(octave)
        name = diatonic_pc_name + str(accidental) + octave.ticks
        return type(self)(name)
