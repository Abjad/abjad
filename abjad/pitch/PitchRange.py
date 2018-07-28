import collections
import copy
import functools
import numbers
from . import constants
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.StorageFormatManager import StorageFormatManager


@functools.total_ordering
class PitchRange(AbjadValueObject):
    """
    Pitch range.

    ..  container:: example

        Pitches from C3 to C7, inclusive:

        >>> pitch_range = abjad.PitchRange('[C3, C7]')
        >>> abjad.show(pitch_range) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(pitch_range)
            abjad.PitchRange('[C3, C7]')

    Initalizes from pitch numbers, pitch names, pitch instances,
    one-line reprs or other pitch range objects.

    Pitch ranges do not sort relative to other pitch ranges.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_start',
        '_stop',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, range_string='[A0, C8]'):
        if isinstance(range_string, type(self)):
            range_string = range_string.range_string
        start, stop = self._parse_range_string(range_string)
        self._start = start
        self._stop = stop

    ### SPECIAL METHODS ###

    def __contains__(self, argument):
        """
        Is true when pitch range contains `argument`.

        ..  container:: example

            Closed / closed range:

            >>> range_ = abjad.PitchRange('[A0, C8]')

            >>> -99 in range_
            False

            >>> -39 in range_
            True

            >>> 0 in range_
            True

            >>> 48 in range_
            True

            >>> 99 in range_
            False

        ..  container:: example

            Closed / open range:

            >>> range_ = abjad.PitchRange('[A0, C8)')

            >>> -99 in range_
            False

            >>> -39 in range_
            True

            >>> 0 in range_
            True

            >>> 48 in range_
            False

            >>> 99 in range_
            False

        ..  container:: example

            Closed / infinite range:

            >>> range_ = abjad.PitchRange('[-39, +inf]')

            >>> -99 in range_
            False

            >>> -39 in range_
            True

            >>> 0 in range_
            True

            >>> 48 in range_
            True

            >>> 99 in range_
            True

        ..  container:: example

            Open / closed range:

            >>> range_ = abjad.PitchRange('(A0, C8]')

            >>> -99 in range_
            False

            >>> -39 in range_
            False

            >>> 0 in range_
            True

            >>> 48 in range_
            True

            >>> 99 in range_
            False

        ..  container:: example

            Open / open range:

            >>> range_ = abjad.PitchRange('(A0, C8)')

            >>> -99 in range_
            False

            >>> -39 in range_
            False

            >>> 0 in range_
            True

            >>> 48 in range_
            False

            >>> 99 in range_
            False

        ..  container:: example

            Infinite / closed range:

            >>> range_ = abjad.PitchRange('[-inf, C8]')

            >>> -99 in range_
            True

            >>> -39 in range_
            True

            >>> 0 in range_
            True

            >>> 48 in range_
            True

            >>> 99 in range_
            False

        ..  container:: example

            Infinite / open range:

            >>> range_ = abjad.PitchRange('[-inf, C8)')

            >>> -99 in range_
            True

            >>> -39 in range_
            True

            >>> 0 in range_
            True

            >>> 48 in range_
            False

            >>> 99 in range_
            False

        ..  container:: example

            Infinite / infinite range:

            >>> range_ = abjad.PitchRange('[-inf, +inf]')

            >>> -99 in range_
            True

            >>> -39 in range_
            True

            >>> 0 in range_
            True

            >>> 48 in range_
            True

            >>> 99 in range_
            True

        Returns true or false.
        """
        import abjad
        if (
            hasattr(argument, '_has_effective_indicator') and
            'unpitched' in abjad.inspect(argument).indicators(str)
            ):
            return True
        elif isinstance(argument, (int, float)):
            pitch = abjad.NamedPitch(argument)
            return self._contains_pitch(pitch)
        elif isinstance(argument, abjad.NamedPitch):
            return self._contains_pitch(argument)
        elif isinstance(argument, abjad.Note):
            sounding_pitch = abjad.inspect(argument).sounding_pitch()
            return self._contains_pitch(sounding_pitch)
        elif isinstance(argument, abjad.Chord):
            sounding_pitches = abjad.inspect(argument).sounding_pitches()
            return all(self._contains_pitch(x) for x in sounding_pitches)
        elif isinstance(argument, (abjad.Rest, abjad.Skip)):
            return True
        elif isinstance(argument, abjad.Container):
            return all(x in self for x in abjad.iterate(argument).leaves())
        else:
            pitches = list(abjad.iterate(argument).pitches())
            if pitches:
                return all(self._contains_pitch(x) for x in pitches)
            else:
                try:
                    return all(self._contains_pitch(x) for x in argument)
                except TypeError:
                    return False
        return False

    def __eq__(self, argument):
        """
        Is true when `argument` is a pitch range with start and stop equal
        to those of this pitch range.

        ..  container:: example

            >>> range_1 = abjad.PitchRange.from_pitches(-39, 0)
            >>> range_2 = abjad.PitchRange.from_pitches(-39, 0)
            >>> range_3 = abjad.PitchRange.from_pitches(-39, 48)

            >>> range_1 == range_1
            True
            >>> range_1 == range_2
            True
            >>> range_1 == range_3
            False

            >>> range_2 == range_1
            True
            >>> range_2 == range_2
            True
            >>> range_2 == range_3
            False

            >>> range_3 == range_1
            False
            >>> range_3 == range_2
            False
            >>> range_3 == range_3
            True

        Returns true or false.
        """
        return super().__eq__(argument)

    def __format__(self, format_specification=''):
        """
        Formats pitch range.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        """
        if format_specification in ('', 'storage'):
            return StorageFormatManager(self).get_storage_format()
        return str(self)

    def __hash__(self):
        """
        Hashes pitch range.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super().__hash__()

    def __illustrate__(self):
        r"""
        Illustrates pitch range.

        ..  container:: example

            >>> pitch_range = abjad.PitchRange('[C3, C7]')
            >>> abjad.show(pitch_range) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = pitch_range.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score])
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override Glissando.thickness = #2
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble Staff"
                        {
                            \clef "treble"
                            s1 * 1/4
                            s1 * 1/4
                        }
                        \context Staff = "Bass Staff"
                        {
                            \clef "bass"
                            c1 * 1/4
                            \glissando
                            \change Staff = "Treble Staff"
                            c''''1 * 1/4
                        }
                    >>
                >>

        Returns LilyPond file.
        """
        import abjad
        start_pitch_clef = abjad.Clef.from_selection(self.start_pitch)
        stop_pitch_clef = abjad.Clef.from_selection(self.stop_pitch)
        start_note = abjad.Note(self.start_pitch, 1)
        stop_note = abjad.Note(self.stop_pitch, 1)
        glissando = abjad.Glissando()
        if start_pitch_clef == stop_pitch_clef:
            if start_pitch_clef == abjad.Clef('bass'):
                bass_staff = abjad.Staff()
                abjad.attach(abjad.Clef('bass'), bass_staff)
                bass_staff.extend([start_note, stop_note])
                bass_leaves = abjad.select(bass_staff).leaves()
                abjad.attach(glissando, bass_leaves)
                score = abjad.Score([bass_staff])
            else:
                treble_staff = abjad.Staff()
                abjad.attach(abjad.Clef('treble'), treble_staff)
                treble_staff.extend([start_note, stop_note])
                treble_leaves = abjad.select(treble_staff).leaves()
                abjad.attach(glissando, treble_leaves)
                score = abjad.Score([treble_staff])
        else:
            result = abjad.Score.make_piano_score()
            score, treble_staff, bass_staff = result
            bass_staff.extend([start_note, stop_note])
            treble_staff.extend(abjad.Skip(1) * 2)
            bass_leaves = abjad.select(bass_staff).leaves()
            abjad.attach(glissando, bass_leaves)
            abjad.attach(abjad.StaffChange(treble_staff), bass_staff[1])
            abjad.attach(abjad.Clef('treble'), treble_staff[0])
            abjad.attach(abjad.Clef('bass'), bass_staff[0])
        for leaf in abjad.iterate(score).leaves():
            abjad.attach(abjad.Multiplier(1, 4), leaf)
        abjad.override(score).bar_line.stencil = False
        abjad.override(score).span_bar.stencil = False
        abjad.override(score).glissando.thickness = 2
        abjad.override(score).time_signature.stencil = False
        lilypond_file = abjad.LilyPondFile.new(score)
        return lilypond_file

    def __lt__(self, argument):
        """
        Is true when start pitch of this pitch-range is less than start
        pitch of `argument` pitch range.

        ..  container:: example

            >>> range_1 = abjad.PitchRange.from_pitches(-39, 0)
            >>> range_2 = abjad.PitchRange.from_pitches(-39, 0)
            >>> range_3 = abjad.PitchRange.from_pitches(-39, 48)

            >>> range_1 < range_1
            False
            >>> range_1 < range_2
            False
            >>> range_1 < range_3
            True

            >>> range_2 < range_1
            False
            >>> range_2 < range_2
            False
            >>> range_2 < range_3
            True

            >>> range_3 < range_1
            False
            >>> range_3 < range_2
            False
            >>> range_3 < range_3
            False

        Returns true or false.
        """
        try:
            argument = type(self)(argument)
        except (TypeError, ValueError):
            return False
        if self.start_pitch == argument.start_pitch:
            return self.stop_pitch < argument.stop_pitch
        return self.start_pitch < argument.start_pitch

    ### PRIVATE PROPERTIES ###

    @property
    def _close_bracket_string(self):
        if self.stop_pitch_is_included_in_range:
            return ']'
        else:
            return ')'

    @property
    def _open_bracket_string(self):
        if self.start_pitch_is_included_in_range:
            return '['
        else:
            return '('

    ### PRIVATE METHODS ###

    def _contains_pitch(self, pitch):
        import abjad
        if isinstance(pitch, numbers.Number):
            pitch = abjad.NamedPitch(pitch)
        elif isinstance(pitch, str):
            pitch = abjad.NamedPitch(pitch)
        if self.start_pitch is None and self.stop_pitch is None:
            return True
        elif self.start_pitch is None:
            if self.stop_pitch_is_included_in_range:
                return pitch <= self.stop_pitch
            else:
                return pitch < self.stop_pitch
        elif self.stop_pitch is None:
            if self.start_pitch_is_included_in_range:
                return self.start_pitch <= pitch
            else:
                return self.start_pitch < pitch
        else:
            if self.start_pitch_is_included_in_range:
                if self.stop_pitch_is_included_in_range:
                    return self.start_pitch <= pitch <= self.stop_pitch
                else:
                    return self.start_pitch <= pitch < self.stop_pitch
            else:
                if self.stop_pitch_is_included_in_range:
                    return self.start_pitch < pitch <= self.stop_pitch
                else:
                    return self.start_pitch < pitch < self.stop_pitch

    def _get_format_specification(self):
        return FormatSpecification(
            self,
            coerce_for_equality=True,
            repr_is_indented=False,
            storage_format_args_values=[self.range_string],
            storage_format_is_indented=False,
            )

    def _get_named_range_string(self):
        result = []
        result.append(self._open_bracket_string)
        if self.start_pitch:
            result.append(self.start_pitch.get_name(locale='us'))
        else:
            result.append('-inf')
        result.append(', ')
        if self.stop_pitch:
            result.append(self.stop_pitch.get_name(locale='us'))
        else:
            result.append('+inf')
        result.append(self._close_bracket_string)
        result = ''.join(result)
        return result

    def _get_numbered_range_string(self):
        result = []
        result.append(self._open_bracket_string)
        result.append(str(self.start_pitch.number))
        result.append(', ')
        result.append(str(self.stop_pitch.number))
        result.append(self._close_bracket_string)
        result = ''.join(result)
        return result

    def _list_numeric_octave_transpositions(self, pitch_number_list):
        result = []
        pitch_number_set = set(pitch_number_list)
        start_pitch_number = self.start_pitch.number
        stop_pitch_number = self.stop_pitch.number
        range_set = set(range(start_pitch_number, stop_pitch_number + 1))
        while pitch_number_set.issubset(range_set):
            next_pitch_number = list(pitch_number_set)
            next_pitch_number.sort()
            result.extend([next_pitch_number])
            pitch_number_set = set([_ + 12 for _ in pitch_number_set])
        pitch_number_set = set([_ - 12 for _ in pitch_number_list])
        while pitch_number_set.issubset(range_set):
            next_pitch_number = list(pitch_number_set)
            next_pitch_number.sort()
            result.extend([next_pitch_number])
            pitch_number_set = set([_ - 12 for _ in pitch_number_set])
        result.sort()
        return result

    def _parse_range_string(self, range_string):
        import abjad
        assert isinstance(range_string, str), repr(range_string)
        range_string = range_string.replace('-inf', '-1000')
        range_string = range_string.replace('+inf', '1000')
        match = constants._range_string_regex.match(range_string)
        if match is None:
            message = 'can not instantiate pitch range: {!r}'
            message = message.format(range_string)
            raise ValueError(message)
        group_dict = match.groupdict()
        start_punctuation = group_dict['open_bracket']
        start_pitch_string = group_dict['start_pitch']
        stop_pitch_string = group_dict['stop_pitch']
        stop_punctuation = group_dict['close_bracket']
        start_inclusivity_string = \
            constants._start_punctuation_to_inclusivity_string[start_punctuation]
        stop_inclusivity_string = \
            constants._stop_punctuation_to_inclusivity_string[stop_punctuation]
        if start_pitch_string == '-1000':
            start_pitch = None
        else:
            try:
                start_pitch = abjad.NamedPitch(start_pitch_string)
            except (TypeError, ValueError):
                start_pitch = abjad.NumberedPitch(int(start_pitch_string))
        if stop_pitch_string == '1000':
            stop_pitch = None
        else:
            try:
                stop_pitch = abjad.NamedPitch(stop_pitch_string)
            except (TypeError, ValueError):
                stop_pitch = abjad.NumberedPitch(int(stop_pitch_string))
        start_pair = (start_pitch, start_inclusivity_string)
        stop_pair = (stop_pitch, stop_inclusivity_string)
        return start_pair, stop_pair

    ### PUBLIC PROPERTIES ###

    @property
    def range_string(self):
        """
        Gets range string of pitch range.

        ..  container:: example

            >>> pitch_range = abjad.PitchRange('[C3, C7]')
            >>> pitch_range.range_string
            '[C3, C7]'

        Returns string.
        """
        return self._get_named_range_string()

    @property
    def start_pitch(self):
        """
        Start pitch of pitch range.

        >>> pitch_range = abjad.PitchRange('[C3, C7]')
        >>> pitch_range.start_pitch
        NamedPitch('c')

        Returns pitch.
        """
        if self._start is None:
            return None
        return self._start[0]

    @property
    def start_pitch_is_included_in_range(self):
        """
        Is true when start pitch is included in range.

        >>> pitch_range = abjad.PitchRange('[C3, C7]')
        >>> pitch_range.start_pitch_is_included_in_range
        True

        Returns true or false.
        """
        if self._start is None:
            return True
        return self._start[1] == 'inclusive'

    @property
    def stop_pitch(self):
        """
        Stop pitch of pitch range.

        >>> pitch_range = abjad.PitchRange('[C3, C7]')
        >>> pitch_range.stop_pitch
        NamedPitch("c''''")

        Returns pitch.
        """
        if self._stop is None:
            return None
        return self._stop[0]

    @property
    def stop_pitch_is_included_in_range(self):
        """
        Is true when stop pitch is included in range.

        >>> pitch_range = abjad.PitchRange('[C3, C7]')
        >>> pitch_range.stop_pitch_is_included_in_range
        True

        Returns true or false.
        """
        if self._stop is None:
            return True
        return self._stop[1] == 'inclusive'

    ### PUBLIC METHODS ###

    @staticmethod
    def from_pitches(
        start_pitch,
        stop_pitch,
        start_pitch_is_included_in_range=True,
        stop_pitch_is_included_in_range=True,
        ):
        """
        Initializes pitch range from numbers.

        ..  container:: example

            >>> abjad.PitchRange.from_pitches(-18, 19)
            PitchRange('[F#2, G5]')

        Returns pitch range.
        """
        import abjad
        if start_pitch is None:
            start_pitch_string = '-inf'
        else:
            start_pitch_string = str(abjad.NamedPitch(start_pitch))
        if stop_pitch is None:
            stop_pitch_string = '+inf'
        else:
            stop_pitch_string = str(abjad.NamedPitch(stop_pitch))
        start_containment = '['
        if not start_pitch_is_included_in_range:
            start_containment = '('
        stop_containment = ']'
        if not stop_pitch_is_included_in_range:
            stop_containment = ')'
        string = '{}{}, {}{}'
        string = string.format(
            start_containment,
            start_pitch_string,
            stop_pitch_string,
            stop_containment,
            )
        pitch_range = PitchRange(string)
        return pitch_range

    @classmethod
    def is_range_string(class_, argument):
        """Is true when `argument` is a pitch range string.

        ..  container:: example

            >>> abjad.PitchRange.is_range_string('[A0, C8]')
            True

            >>> abjad.PitchRange.is_range_string('[A#0, Cb~8]')
            True

            >>> abjad.PitchRange.is_range_string('[A#+0, cs'')')
            True

            >>> abjad.PitchRange.is_range_string('(b,,,, ctqs]')
            True

        ..  container:: example

            >>> abjad.PitchRange.is_range_string('text')
            False

        The regex that underlies this predicate matches against two
        comma-separated pitches enclosed in some combination of square
        brackets and round parentheses.

        Returns true or false.
        """
        if not isinstance(argument, str):
            return False
        return bool(constants._range_string_regex.match(argument))

    def list_octave_transpositions(self, pitch_carrier):
        """
        Lists octave transpositions of `pitch_carrier` in pitch range.

        ..  container:: example

            Lists octave transpositions of three-pitch chord:

            >>> chord = abjad.Chord("<c' d' e'>4")
            >>> pitch_range = abjad.PitchRange.from_pitches(0, 48)
            >>> result = pitch_range.list_octave_transpositions(chord)

            >>> for chord in result:
            ...     chord
            ...
            Chord("<c' d' e'>4")
            Chord("<c'' d'' e''>4")
            Chord("<c''' d''' e'''>4")
            Chord("<c'''' d'''' e''''>4")

        Returns a list of `pitch_carrier` objects.
        """
        import abjad
        if isinstance(pitch_carrier, collections.Iterable):
            if all(isinstance(x, (int, float)) for x in pitch_carrier):
                return self._list_numeric_octave_transpositions(pitch_carrier)
        prototype = (abjad.Chord, abjad.PitchSet)
        if not isinstance(pitch_carrier, prototype):
            message = 'must be chord or pitch-set: {!r}'
            message = message.format(pitch_carrier)
            raise TypeError(message)
        result = []
        interval = abjad.NumberedInterval(-12)
        while True:
            pitch_carrier_copy = copy.copy(pitch_carrier)
            candidate = interval.transpose(pitch_carrier_copy)
            if candidate in self:
                result.append(candidate)
                interval -= 12
            else:
                break
        result.reverse()
        interval = abjad.NumberedInterval(0)
        while True:
            pitch_carrier_copy = copy.copy(pitch_carrier)
            candidate = interval.transpose(pitch_carrier_copy)
            if candidate in self:
                result.append(candidate)
                interval += abjad.NumberedInterval(12)
            else:
                break
        return result

    def voice_pitch_class(self, pitch_class):
        """
        Voices `pitch_class`:

        ..  container:: example

            Voices C three times:

            >>> pitch_range = abjad.PitchRange('[C4, C6]')
            >>> pitch_range.voice_pitch_class('c')
            (NamedPitch("c'"), NamedPitch("c''"), NamedPitch("c'''"))

        ..  container:: example

            Voices B two times:

            >>> pitch_range = abjad.PitchRange('[C4, C6]')
            >>> pitch_range.voice_pitch_class('b')
            (NamedPitch("b'"), NamedPitch("b''"))

        ..  container:: example

            Returns empty because B can not voice:

            >>> pitch_range = abjad.PitchRange('[C4, A4)')
            >>> pitch_range.voice_pitch_class('b')
            ()

        Returns tuple of zero or more named pitches.
        """
        import abjad
        named_pitch_class = abjad.NamedPitchClass(pitch_class)
        pair = (named_pitch_class.name, self.start_pitch.octave.number)
        named_pitch = abjad.NamedPitch(pair)
        result = []
        while named_pitch <= self.stop_pitch:
            if named_pitch in self:
                result.append(named_pitch)
            named_pitch += 12
        return tuple(result)
