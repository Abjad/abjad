import functools
import numbers
import typing

from ..storage import FormatSpecification, StorageFormatManager
from . import _lib
from .Octave import Octave
from .pitchclasses import NamedPitchClass
from .pitches import NamedPitch, NumberedPitch, Pitch


@functools.total_ordering
class PitchRange:
    r"""
    Pitch range.

    ..  container:: example

        Pitches from C3 to C7, inclusive:

        >>> pitch_range = abjad.PitchRange("[C3, C7]")
        >>> lilypond_file = abjad.illustrate(pitch_range)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.storage(pitch_range)
            >>> print(string)
            abjad.PitchRange('[C3, C7]')

    ..  container:: example

        >>> pitch_range = abjad.PitchRange("[C3, C7]")
        >>> lilypond_file = abjad.illustrate(pitch_range)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            \with
            {
                \override BarLine.stencil = ##f
                \override Glissando.thickness = 2
                \override SpanBar.stencil = ##f
                \override TimeSignature.stencil = ##f
            }
            <<
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        s1 * 1/4
                        s1 * 1/4
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        c1 * 1/4
                        \glissando
                        \change Staff = Treble_Staff
                        c''''1 * 1/4
                    }
                >>
            >>

    Initalizes from pitch numbers, pitch names, pitch instances,
    one-line reprs or other pitch range objects.

    Pitch ranges do not sort relative to other pitch ranges.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_start", "_stop")

    ### INITIALIZER ###

    def __init__(self, range_string="[A0, C8]"):
        if isinstance(range_string, type(self)):
            range_string = range_string.range_string
        start, stop = self._parse_range_string(range_string)
        self._start = start
        self._stop = stop

    ### SPECIAL METHODS ###

    def __contains__(self, argument) -> bool:
        """
        Is true when pitch range contains ``argument``.

        ..  container:: example

            Closed / closed range:

            >>> range_ = abjad.PitchRange("[A0, C8]")

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

            >>> range_ = abjad.PitchRange("[A0, C8)")

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

            >>> range_ = abjad.PitchRange("[-39, +inf]")

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

            >>> range_ = abjad.PitchRange("(A0, C8]")

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

            >>> range_ = abjad.PitchRange("(A0, C8)")

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

            >>> range_ = abjad.PitchRange("[-inf, C8]")

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

            >>> range_ = abjad.PitchRange("[-inf, C8)")

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

            >>> range_ = abjad.PitchRange("[-inf, +inf]")

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

        """
        if isinstance(argument, (int, float)):
            pitch = NamedPitch(argument)
            return self._contains_pitch(pitch)
        if isinstance(argument, Pitch):
            return self._contains_pitch(argument)
        raise Exception(f"must be pitch or number {argument!r}.")

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a pitch range with start and stop equal
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
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self):
        """
        Hashes pitch range.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __lt__(self, argument):
        """
        Is true when start pitch of this pitch-range is less than start
        pitch of ``argument`` pitch range.

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

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE PROPERTIES ###

    @property
    def _close_bracket_string(self):
        if self.stop_pitch_is_included_in_range:
            return "]"
        else:
            return ")"

    @property
    def _open_bracket_string(self):
        if self.start_pitch_is_included_in_range:
            return "["
        else:
            return "("

    ### PRIVATE METHODS ###

    def _contains_pitch(self, pitch):
        if isinstance(pitch, numbers.Number):
            pitch = NamedPitch(pitch)
        elif isinstance(pitch, str):
            pitch = NamedPitch(pitch)
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
            result.append(self.start_pitch.get_name(locale="us"))
        else:
            result.append("-inf")
        result.append(", ")
        if self.stop_pitch:
            result.append(self.stop_pitch.get_name(locale="us"))
        else:
            result.append("+inf")
        result.append(self._close_bracket_string)
        result = "".join(result)
        return result

    def _get_numbered_range_string(self):
        result = []
        result.append(self._open_bracket_string)
        result.append(str(self.start_pitch.number))
        result.append(", ")
        result.append(str(self.stop_pitch.number))
        result.append(self._close_bracket_string)
        result = "".join(result)
        return result

    def _parse_range_string(self, range_string):
        assert isinstance(range_string, str), repr(range_string)
        range_string = range_string.replace("-inf", "-1000")
        range_string = range_string.replace("+inf", "1000")
        match = _lib._range_string_regex.match(range_string)
        if match is None:
            raise ValueError(f"can not instantiate pitch range: {range_string!r}")
        group_dict = match.groupdict()
        start_punctuation = group_dict["open_bracket"]
        start_pitch_string = group_dict["start_pitch"]
        stop_pitch_string = group_dict["stop_pitch"]
        stop_punctuation = group_dict["close_bracket"]
        start_inclusivity_string = _lib._start_punctuation_to_inclusivity_string[
            start_punctuation
        ]
        stop_inclusivity_string = _lib._stop_punctuation_to_inclusivity_string[
            stop_punctuation
        ]
        if start_pitch_string == "-1000":
            start_pitch = None
        else:
            try:
                start_pitch = NamedPitch(start_pitch_string)
            except (TypeError, ValueError):
                start_pitch = NumberedPitch(int(start_pitch_string))
        if stop_pitch_string == "1000":
            stop_pitch = None
        else:
            try:
                stop_pitch = NamedPitch(stop_pitch_string)
            except (TypeError, ValueError):
                stop_pitch = NumberedPitch(int(stop_pitch_string))
        start_pair = (start_pitch, start_inclusivity_string)
        stop_pair = (stop_pitch, stop_inclusivity_string)
        return start_pair, stop_pair

    ### PUBLIC PROPERTIES ###

    @property
    def range_string(self) -> str:
        """
        Gets range string of pitch range.

        ..  container:: example

            >>> pitch_range = abjad.PitchRange("[C3, C7]")
            >>> pitch_range.range_string
            '[C3, C7]'

        """
        return self._get_named_range_string()

    @property
    def start_pitch(self) -> typing.Optional[NamedPitch]:
        """
        Start pitch of pitch range.

        ..  container:: example

            >>> pitch_range = abjad.PitchRange("[C3, C7]")
            >>> pitch_range.start_pitch
            NamedPitch('c')

        """
        if self._start is None:
            return None
        return self._start[0]

    @property
    def start_pitch_is_included_in_range(self) -> bool:
        """
        Is true when start pitch is included in range.

        ..  container:: example

            >>> pitch_range = abjad.PitchRange("[C3, C7]")
            >>> pitch_range.start_pitch_is_included_in_range
            True

        """
        if self._start is None:
            return True
        return self._start[1] == "inclusive"

    @property
    def stop_pitch(self) -> typing.Optional[NamedPitch]:
        """
        Stop pitch of pitch range.

        ..  container:: example

            >>> pitch_range = abjad.PitchRange("[C3, C7]")
            >>> pitch_range.stop_pitch
            NamedPitch("c''''")

        """
        if self._stop is None:
            return None
        return self._stop[0]

    @property
    def stop_pitch_is_included_in_range(self) -> bool:
        """
        Is true when stop pitch is included in range.

        ..  container:: example

            >>> pitch_range = abjad.PitchRange("[C3, C7]")
            >>> pitch_range.stop_pitch_is_included_in_range
            True

        """
        if self._stop is None:
            return True
        return self._stop[1] == "inclusive"

    ### PUBLIC METHODS ###

    @staticmethod
    def from_octave(octave) -> "PitchRange":
        """
        Initializes pitch range from octave.

        ..  container:: example

            >>> abjad.PitchRange.from_octave(5)
            PitchRange('[C5, C6)')

        """
        octave = Octave(octave)
        return PitchRange(f"[C{octave.number}, C{octave.number + 1})")

    @staticmethod
    def from_pitches(
        start_pitch,
        stop_pitch,
        start_pitch_is_included_in_range=True,
        stop_pitch_is_included_in_range=True,
    ) -> "PitchRange":
        """
        Initializes pitch range from numbers.

        ..  container:: example

            >>> abjad.PitchRange.from_pitches(-18, 19)
            PitchRange('[F#2, G5]')

        """
        if start_pitch is None:
            start_pitch_string = "-inf"
        else:
            start_pitch_string = str(NamedPitch(start_pitch))
        if stop_pitch is None:
            stop_pitch_string = "+inf"
        else:
            stop_pitch_string = str(NamedPitch(stop_pitch))
        start_containment = "["
        if not start_pitch_is_included_in_range:
            start_containment = "("
        stop_containment = "]"
        if not stop_pitch_is_included_in_range:
            stop_containment = ")"
        string = "{}{}, {}{}"
        string = string.format(
            start_containment,
            start_pitch_string,
            stop_pitch_string,
            stop_containment,
        )
        pitch_range = PitchRange(string)
        return pitch_range

    @classmethod
    def is_range_string(class_, argument) -> bool:
        """Is true when ``argument`` is a pitch range string.

        ..  container:: example

            >>> abjad.PitchRange.is_range_string("[A0, C8]")
            True

            >>> abjad.PitchRange.is_range_string("[A#0, Cb~8]")
            True

            >>> abjad.PitchRange.is_range_string("[A#+0, cs'')")
            True

            >>> abjad.PitchRange.is_range_string("(b,,,, ctqs]")
            True

        ..  container:: example

            >>> abjad.PitchRange.is_range_string("text")
            False

        The regex that underlies this predicate matches against two
        comma-separated pitches enclosed in some combination of square
        brackets and round parentheses.
        """
        if not isinstance(argument, str):
            return False
        return bool(_lib._range_string_regex.match(argument))

    def voice_pitch_class(self, pitch_class):
        """
        Voices ``pitch_class``:

        ..  container:: example

            Voices C three times:

            >>> pitch_range = abjad.PitchRange("[C4, C6]")
            >>> pitch_range.voice_pitch_class("c")
            (NamedPitch("c'"), NamedPitch("c''"), NamedPitch("c'''"))

        ..  container:: example

            Voices B two times:

            >>> pitch_range = abjad.PitchRange("[C4, C6]")
            >>> pitch_range.voice_pitch_class("b")
            (NamedPitch("b'"), NamedPitch("b''"))

        ..  container:: example

            Returns empty because B can not voice:

            >>> pitch_range = abjad.PitchRange("[C4, A4)")
            >>> pitch_range.voice_pitch_class('b')
            ()

        """
        named_pitch_class = NamedPitchClass(pitch_class)
        assert self.start_pitch is not None
        assert self.stop_pitch is not None
        pair = (named_pitch_class.name, self.start_pitch.octave.number)
        named_pitch = NamedPitch(pair)
        result = []
        while named_pitch <= self.stop_pitch:
            if named_pitch in self:
                result.append(named_pitch)
            named_pitch += 12
        return tuple(result)
