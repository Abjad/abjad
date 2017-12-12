import math
import numbers
from abjad.tools.pitchtools.Pitch import Pitch


class NamedPitch(Pitch):
    r'''Named pitch.

    ..  container:: example

        Initializes from pitch name:

        >>> pitch = abjad.NamedPitch("cs''")
        >>> abjad.show(pitch) # doctest: +SKIP

        ..  docs::

            >>> staff = pitch.__illustrate__()[abjad.Staff]
            >>> abjad.f(staff)
            \new Staff \with {
                \override TimeSignature.stencil = ##f
            } {
                \clef "treble"
                cs''1 * 1/4
            }

        Initializes quartertone from pitch name:

        >>> pitch = abjad.NamedPitch("aqs")
        >>> abjad.show(pitch) # doctest: +SKIP

        ..  docs::

            >>> staff = pitch.__illustrate__()[abjad.Staff]
            >>> abjad.f(staff)
            \new Staff \with {
                \override TimeSignature.stencil = ##f
            } {
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
            \new Staff \with {
                \override TimeSignature.stencil = ##f
            } {
                \clef "treble"
                cs''1 * 1/4
            }

        Initializes quartertone from pitch-class / octave string:

        >>> pitch = abjad.NamedPitch('A+3')
        >>> abjad.show(pitch) # doctest: +SKIP

        ..  docs::

            >>> staff = pitch.__illustrate__()[abjad.Staff]
            >>> abjad.f(staff)
            \new Staff \with {
                \override TimeSignature.stencil = ##f
            } {
                \clef "bass"
                aqs1 * 1/4
            }

        >>> pitch = abjad.NamedPitch('Aqs3')
        >>> abjad.show(pitch) # doctest: +SKIP

        ..  docs::

            >>> staff = pitch.__illustrate__()[abjad.Staff]
            >>> abjad.f(staff)
            \new Staff \with {
                \override TimeSignature.stencil = ##f
            } {
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
            \new Staff \with {
                \override TimeSignature.stencil = ##f
            } {
                \once \override Accidental.stencil = #ly:text-interface::print
                \once \override Accidental.text = \markup { \musicglyph #"accidentals.sharp.arrowup" }
                \clef "treble"
                cs''1 * 1/4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_name',
        )

    ### INITIALIZER ###

    def __init__(self, name="c'", arrow=None):
        import abjad
        if self._is_pitch_name(name):
            pass
        elif self._is_pitch_class_octave_number_string(name):
            name = self._american_name_to_lilypond_name(name)
        elif isinstance(name, type(self)):
            arrow = name.arrow
            name = name.name
        elif isinstance(name, abjad.NamedPitchClass):
            name = name.name + "'"
        elif isinstance(name, tuple) and len(name) == 2:
            pitch_class, octave = name
            pitch_class = abjad.NamedPitchClass(pitch_class)
            octave = abjad.Octave(octave)
            name = str(pitch_class) + str(abjad.Octave(octave))
        elif isinstance(name, numbers.Number) or hasattr(name, 'number'):
            number = getattr(name, 'number', name)
            named_pitch_class = abjad.NamedPitchClass(number)
            octave = number // 12 + 4
            name = named_pitch_class.name + abjad.Octave(octave).ticks
        elif isinstance(name, abjad.Note):
            name = name.written_pitch.name
        else:
            message = 'can not initialize {} from {!r}.'
            message = message.format(type(self).__name__, name)
            raise ValueError(message)
        assert self._is_pitch_name(name)
        self._name = name
        if arrow not in (abjad.Up, abjad.Down, None):
            message = 'arrow must be up, down or none: {!r}.'
            message = message.format(arrow)
            raise TypeError(message)
        if not hasattr(self, '_arrow'):
            self._arrow = arrow

    ### SPECIAL METHODS ###

    def __add__(self, interval):
        r'''Adds named pitch to `interval`.

        ..  container:: example

            >>> abjad.NamedPitch("cs''") + abjad.NamedInterval('-M2')
            NamedPitch("b'")

            >>> abjad.NamedPitch("cs''") + abjad.NamedInterval('P1')
            NamedPitch("cs''")

            >>> abjad.NamedPitch("cs''") + abjad.NamedInterval('+M2')
            NamedPitch("ds''")

        Returns new named pitch.
        '''
        import abjad
        interval = abjad.NamedInterval(interval)
        return interval.transpose(self)

    def __copy__(self, *arguments):
        r'''Copies named pitch.

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
        '''
        return type(self)(self, arrow=self.arrow)

    def __eq__(self, argument):
        r'''Is true when `argument` is a named pitch equal to this named pitch.
        Otherwise false.

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
        '''
        return super(NamedPitch, self).__eq__(argument)

    def __hash__(self):
        r'''Hashes named pitch.

        Returns integer.
        '''
        return super(NamedPitch, self).__hash__()

    def __lt__(self, argument):
        r'''Is true when named pitch is less than `argument`. Otherwise false.

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
        '''
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
        r'''Right-addition not defined on named pitches.

        ..  container:: example

            >>> abjad.NamedPitch("cs'").__radd__(1)
            Traceback (most recent call last):
            ...
            NotImplementedError: right-addition not defined on NamedPitch.

        '''
        message = 'right-addition not defined on {}.'
        message = message.format(type(self).__name__)
        raise NotImplementedError(message)

    def __str__(self):
        r'''Gets string representation of named pitch.

        ..  container:: example

            >>> str(abjad.NamedPitch("c''"))
            "c''"

            >>> str(abjad.NamedPitch("cs''"))
            "cs''"

            >>> str(abjad.NamedPitch("df''"))
            "df''"

        Returns string.
        '''
        return self.name

    def __sub__(self, argument):
        r'''Subtracts `argument` from named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("cs''") - abjad.NamedPitch("b'")
            NamedInterval('-M2')

            >>> abjad.NamedPitch("cs''") - abjad.NamedPitch("fs''")
            NamedInterval('+P4')

        Returns named interval.
        '''
        import abjad
        if isinstance(argument, type(self)):
            return abjad.NamedInterval.from_pitch_carriers(self, argument)
        interval = abjad.NamedInterval(argument)
        interval = -interval
        return interval.transpose(self)

    ### PRIVATE METHODS ###

    @staticmethod
    def _american_name_to_lilypond_name(name):
        import abjad
        match = NamedPitch._pitch_class_octave_number_regex.match(name)
        group_dict = match.groupdict()
        name = abjad.NamedPitchClass(name).name
        name += abjad.Octave(int(group_dict['octave_number'])).ticks
        return name

    def _apply_accidental(self, accidental):
        import abjad
        name = self._get_diatonic_pitch_class_name()
        name += str(self.accidental + abjad.Accidental(accidental))
        name += self.octave.ticks
        return type(self)(name)

    def _get_alteration(self):
        return self.accidental.semitones

    def _get_diatonic_pitch_class_name(self):
        return self._parse_name()[0]

    def _get_diatonic_pitch_class_number(self):
        import abjad
        diatonic_pitch_class_name = self._get_diatonic_pitch_class_name()
        class_ = abjad.PitchClass
        diatonic_pitch_class_number = (
            class_._diatonic_pitch_class_name_to_diatonic_pitch_class_number[
                diatonic_pitch_class_name]
            )
        return diatonic_pitch_class_number

    def _get_diatonic_pitch_name(self):
        diatonic_pitch_class_name, accidental, ticks = self._parse_name()
        return diatonic_pitch_class_name + ticks

    def _get_diatonic_pitch_number(self):
        diatonic_pitch_number = 7 * (self.octave.number - 4)
        diatonic_pitch_number += self._get_diatonic_pitch_class_number()
        return diatonic_pitch_number

    def _get_format_specification(self):
        import abjad
        return abjad.FormatSpecification(
            self,
            coerce_for_equality=True,
            repr_is_indented=False,
            storage_format_args_values=[self.name],
            storage_format_is_indented=False,
            storage_format_kwargs_names=['arrow'],
            )

    def _get_lilypond_format(self):
        return str(self)

    def _get_pitch_class_name(self):
        parts = self._parse_name()
        return parts[0] + parts[1]

    def _list_format_contributions(self):
        contributions = []
        if self.arrow is None:
            return contributions
        override_string = r'\once \override Accidental.stencil ='
        override_string += ' #ly:text-interface::print'
        contributions.append(override_string)
        string = 'accidentals.{}.arrow{}'
        string = string.format(self.accidental.name, str(self.arrow).lower())
        override_string = r'\once \override Accidental.text ='
        override_string += r' \markup {{ \musicglyph #"{}" }}'
        override_string = override_string.format(string)
        contributions.append(override_string)
        return contributions

    def _parse_name(self):
        match = self._pitch_name_regex.match(self.name)
        if match is None:
            raise Exception(repr(self.name))
        groups = match.groups()
        assert len(groups) == 5, repr(groups)
        diatonic_pitch_class_name = groups[0]
        accidental_abbreviation = groups[1]
        groups[2] is None
        groups[3] is None
        ticks = groups[4]
        return diatonic_pitch_class_name, accidental_abbreviation, ticks

    def _respell_with_flats(self):
        import abjad
        class_ = abjad.PitchClass
        name = class_._pitch_class_number_to_pitch_class_name_with_flats[
            self.pitch_class.number
            ]
        pitch = type(self)((name, self.octave.number))
        return pitch

    def _respell_with_sharps(self):
        import abjad
        class_ = abjad.PitchClass
        name = class_._pitch_class_number_to_pitch_class_name_with_sharps[
            self.pitch_class.number
            ]
        pitch = type(self)((name, self.octave.number))
        return pitch

    @staticmethod
    def _to_nearest_octave(pitch_number, pitch_class_number):
        target_pc = pitch_number % 12
        down = (target_pc - pitch_class_number) % 12
        up = (pitch_class_number - target_pc) % 12
        if up < down:
            return pitch_number + up
        else:
            return pitch_number - down

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        r'''Gets accidental of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").accidental
            Accidental('natural')

            >>> abjad.NamedPitch("cs''").accidental
            Accidental('sharp')

            >>> abjad.NamedPitch("df''").accidental
            Accidental('flat')

        Returns accidental.
        '''
        import abjad
        return abjad.Accidental(self._parse_name()[1])

    @property
    def arrow(self):
        r'''Gets arrow of named pitch.

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
        '''
        return self._arrow

    @property
    def hertz(self):
        r'''Gets frequency of named pitch in Hertz.

        ..  container:: example

            >>> abjad.NamedPitch("c''").hertz
            523.25...

            >>> abjad.NamedPitch("cs''").hertz
            554.36...

            >>> abjad.NamedPitch("df''").hertz
            554.36...

        Returns float.
        '''
        return super(NamedPitch, self).hertz

    @property
    def name(self):
        r'''Gets name of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").name
            "c''"

            >>> abjad.NamedPitch("cs''").name
            "cs''"

            >>> abjad.NamedPitch("df''").name
            "df''"

        Returns string.
        '''
        return self._name

    @property
    def number(self):
        r'''Gets number of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").number
            12

            >>> abjad.NamedPitch("cs''").number
            13

            >>> abjad.NamedPitch("df''").number
            13

        Returns number.
        '''
        import abjad
        number = 12 * (self.octave.number - 4)
        class_ = abjad.PitchClass
        number += class_._diatonic_pitch_class_name_to_pitch_class_number[
            self._get_diatonic_pitch_class_name()
            ]
        number += self._get_alteration()
        return number

    @property
    def octave(self):
        r'''Gets octave of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").octave
            Octave(5)

            >>> abjad.NamedPitch("cs''").octave
            Octave(5)

            >>> abjad.NamedPitch("df''").octave
            Octave(5)

        Returns octave.
        '''
        import abjad
        return abjad.Octave(self._parse_name()[2])

    @property
    def pitch_class(self):
        r'''Gets pitch-class of named pitch.

        ..  container:: example

            >>> abjad.NamedPitch("c''").pitch_class
            NamedPitchClass('c')

            >>> abjad.NamedPitch("cs''").pitch_class
            NamedPitchClass('cs')

            >>> abjad.NamedPitch("df''").pitch_class
            NamedPitchClass('df')

        Returns named pitch-class.
        '''
        import abjad
        return abjad.NamedPitchClass(self._get_pitch_class_name())

    ### PUBLIC METHODS ###

    @classmethod
    def from_hertz(class_, hertz):
        r'''Makes named pitch from `hertz`.

        ..  container:: example

            >>> abjad.NamedPitch.from_hertz(440)
            NamedPitch("a'")

            >>> abjad.NamedPitch.from_hertz(519)
            NamedPitch("c'")

        Returns newly constructed named pitch.
        '''
        return super(NamedPitch, class_).from_hertz(hertz)

    @classmethod
    def from_pitch_carrier(class_, pitch_carrier):
        r'''Makes named pitch from `pitch_carrier`.

        ..  container:: example

            Makes named pitch from named pitch:

            >>> pitch = abjad.NamedPitch(('df', 5))
            >>> abjad.NamedPitch.from_pitch_carrier(pitch)
            NamedPitch("df''")

        ..  container:: example

            Makes named pitch from note:

            >>> note = abjad.Note("df''4")
            >>> abjad.NamedPitch.from_pitch_carrier(note)
            NamedPitch("df''")

        ..  container:: example

            Makes named pitch from note-head:

            >>> note = abjad.Note("df''4")
            >>> abjad.NamedPitch.from_pitch_carrier(note.note_head)
            NamedPitch("df''")

        ..  container:: example

            Makes named pitch from chord:

            >>> chord = abjad.Chord("<df''>4")
            >>> abjad.NamedPitch.from_pitch_carrier(chord)
            NamedPitch("df''")

        ..  container:: example

            Makes named pitch from integer:

            >>> abjad.NamedPitch.from_pitch_carrier(13)
            NamedPitch("cs''")

        ..  container:: example

            Makes named pitch from numbered pitch-class:

            >>> pitch_class = abjad.NumberedPitchClass(7)
            >>> abjad.NamedPitch.from_pitch_carrier(pitch_class)
            NamedPitch("g'")

        Raises value error when `pitch_carrier` carries no pitch.

        Raises value error when `pitch_carrier` carries more than one pitch.

        Returns new named pitch.
        '''
        return super(NamedPitch, class_).from_pitch_carrier(pitch_carrier)

    @classmethod
    def from_pitch_number(
        class_,
        pitch_number,
        diatonic_pitch_class_name,
        ):
        r'''Makes named pitch from `pitch_number`.

        ..  container:: example

            >>> abjad.NamedPitch.from_pitch_number(12, 'b')
            NamedPitch("bs'")
            >>> abjad.NamedPitch.from_pitch_number(12, 'c')
            NamedPitch("c''")
            >>> abjad.NamedPitch.from_pitch_number(12, 'd')
            NamedPitch("dff''")

        ..  container:: example


            >>> abjad.NamedPitch.from_pitch_number(13, 'b')
            NamedPitch("bss'")
            >>> abjad.NamedPitch.from_pitch_number(13, 'c')
            NamedPitch("cs''")
            >>> abjad.NamedPitch.from_pitch_number(13, 'd')
            NamedPitch("df''")

        ..  container:: example


            >>> abjad.NamedPitch.from_pitch_number(14, 'c')
            NamedPitch("css''")
            >>> abjad.NamedPitch.from_pitch_number(14, 'd')
            NamedPitch("d''")
            >>> abjad.NamedPitch.from_pitch_number(14, 'e')
            NamedPitch("eff''")

        Returns new named pitch.
        '''
        import abjad
        pc = abjad.PitchClass._diatonic_pitch_class_name_to_pitch_class_number[
            diatonic_pitch_class_name
            ]
        nearest_neighbor = class_._to_nearest_octave(pitch_number, pc)
        semitones = pitch_number - nearest_neighbor
        accidental = abjad.Accidental(semitones)
        octave = int(math.floor((pitch_number - semitones) / 12)) + 4
        octave = abjad.Octave(octave)
        name = diatonic_pitch_class_name + str(accidental) + octave.ticks
        return class_(name)

    def get_name(self, locale=None):
        r'''Gets name of named pitch according to `locale`.

        ..  container:: example

            >>> abjad.NamedPitch("cs''").get_name()
            "cs''"

            >>> abjad.NamedPitch("cs''").get_name(locale='us')
            'C#5'

        Set `locale` to `'us'` or none.

        Returns string.
        '''
        if locale is None:
            return self.name
        elif locale == 'us':
            return '{}{}{}'.format(
                self._get_diatonic_pitch_class_name().upper(),
                self.accidental.symbol,
                self.octave.number,
                )
        else:
            message = "must be 'us' or none: {!r}."
            message = message.format(locale)
            raise ValueError(message)

    def invert(self, axis=None):
        r'''Inverts named pitch around `axis`.

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
        '''
        return super(NamedPitch, self).invert(axis=axis)

    def multiply(self, n=1):
        r'''Multiplies named pitch.

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
        '''
        return super(NamedPitch, self).multiply(n=n)

    # TODO: duplicate on NumberedPitch
    def to_staff_position(self, clef=None):
        r'''Changes named pitch to staff position.

        ..  container:: example

            Changes C#5 to absolute staff position:

            >>> abjad.NamedPitch('C#5').to_staff_position()
            StaffPosition(7)

        ..  container:: example

            Changes C#5 to treble staff position:


                >>> abjad.NamedPitch('C#5').to_staff_position(clef=abjad.Clef('treble'))
                StaffPosition(1)

        ..  container:: example

            Changes C#5 to bass staff position:


                >>> abjad.NamedPitch('C#5').to_staff_position(clef=abjad.Clef('bass'))
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
                \new Staff \with {
                    \override TextScript.staff-padding = #5
                } {
                    g16 - \markup { -3 }
                    a16 - \markup { -2 }
                    b16 - \markup { -1 }
                    c'16 - \markup { 0 }
                    d'16 - \markup { 1 }
                    e'16 - \markup { 2 }
                    f'16 - \markup { 3 }
                    g'16 - \markup { 4 }
                    a'16 - \markup { 5 }
                    b'16 - \markup { 6 }
                    c''16 - \markup { 7 }
                    d''16 - \markup { 8 }
                    e''16 - \markup { 9 }
                    f''16 - \markup { 10 }
                    g''16 - \markup { 11 }
                    a''16 - \markup { 12 }
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
                \new Staff \with {
                    \override TextScript.staff-padding = #5
                } {
                    g16 - \markup { -9 }
                    a16 - \markup { -8 }
                    b16 - \markup { -7 }
                    c'16 - \markup { -6 }
                    d'16 - \markup { -5 }
                    e'16 - \markup { -4 }
                    f'16 - \markup { -3 }
                    g'16 - \markup { -2 }
                    a'16 - \markup { -1 }
                    b'16 - \markup { 0 }
                    c''16 - \markup { 1 }
                    d''16 - \markup { 2 }
                    e''16 - \markup { 3 }
                    f''16 - \markup { 4 }
                    g''16 - \markup { 5 }
                    a''16 - \markup { 6 }
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
                \new Staff \with {
                    \override TextScript.staff-padding = #5
                } {
                    \clef "bass"
                    g,16 - \markup { -4 }
                    a,16 - \markup { -3 }
                    b,16 - \markup { -2 }
                    c16 - \markup { -1 }
                    d16 - \markup { 0 }
                    e16 - \markup { 1 }
                    f16 - \markup { 2 }
                    g16 - \markup { 3 }
                    a16 - \markup { 4 }
                    b16 - \markup { 5 }
                    c'16 - \markup { 6 }
                    d'16 - \markup { 7 }
                    e'16 - \markup { 8 }
                    f'16 - \markup { 9 }
                    g'16 - \markup { 10 }
                    a'16 - \markup { 11 }
                }

        Returns staff position.
        '''
        import abjad
        staff_position_number = self._get_diatonic_pitch_number()
        if clef is not None:
            staff_position_number += clef.middle_c_position.number
        staff_position = abjad.StaffPosition(staff_position_number)
        return staff_position

    # TODO: combine with transpose_staff_position()
    def transpose(self, n=0):
        r'''Transposes named pitch by index `n`.

        ..  container:: example

            Transposes C4 up a minor second:

            >>> abjad.NamedPitch("c'").transpose(n='m2')
            NamedPitch("df'")

        ..  container:: example

            Transposes C4 down a major second:

            >>> abjad.NamedPitch("c'").transpose(n='-M2')
            NamedPitch('bf')

        Returns new named pitch.
        '''
        import abjad
        interval = abjad.NamedInterval(n)
        return interval.transpose(self)

    # TODO: combine with transpose()
    def transpose_staff_position(self, staff_positions, interval):
        '''Transposes named pitch by `staff_positions` and `interval`.

        ..  container:: example

            Transposes middle C but leaves at same staff position:

            >>> pitch = abjad.NamedPitch(0)

            >>> pitch.transpose_staff_position(0, -2)
            NamedPitch("cff'")
            >>> pitch.transpose_staff_position(0, -1.5)
            NamedPitch("ctqf'")
            >>> pitch.transpose_staff_position(0, -1)
            NamedPitch("cf'")
            >>> pitch.transpose_staff_position(0, -0.5)
            NamedPitch("cqf'")
            >>> pitch.transpose_staff_position(0, 0)
            NamedPitch("c'")
            >>> pitch.transpose_staff_position(0, 0.5)
            NamedPitch("cqs'")
            >>> pitch.transpose_staff_position(0, 1)
            NamedPitch("cs'")
            >>> pitch.transpose_staff_position(0, 1.5)
            NamedPitch("ctqs'")

        ..  container:: example

            Transposes middle C and then respells up 1 staff position:

            >>> pitch.transpose_staff_position(1, 0)
            NamedPitch("dff'")
            >>> pitch.transpose_staff_position(1, 0.5)
            NamedPitch("dtqf'")
            >>> pitch.transpose_staff_position(1, 1)
            NamedPitch("df'")
            >>> pitch.transpose_staff_position(1, 1.5)
            NamedPitch("dqf'")
            >>> pitch.transpose_staff_position(1, 2)
            NamedPitch("d'")
            >>> pitch.transpose_staff_position(1, 2.5)
            NamedPitch("dqs'")
            >>> pitch.transpose_staff_position(1, 3)
            NamedPitch("ds'")
            >>> pitch.transpose_staff_position(1, 3.5)
            NamedPitch("dtqs'")
            >>> pitch.transpose_staff_position(1, 4)
            NamedPitch("dss'")

        Returns new named pitch.
        '''
        import abjad
        pitch_number = self.number + interval
        diatonic_pitch_class_number = self._get_diatonic_pitch_class_number()
        diatonic_pitch_class_number += staff_positions
        diatonic_pitch_class_number %= 7
        class_ = abjad.PitchClass
        dictionary = \
            class_._diatonic_pitch_class_number_to_diatonic_pitch_class_name
        diatonic_pitch_class_name = dictionary[diatonic_pitch_class_number]
        return type(self).from_pitch_number(
            pitch_number,
            diatonic_pitch_class_name,
            )
