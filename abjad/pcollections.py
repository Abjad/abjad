import collections
import copy
import dataclasses
import functools
import importlib
import types
import typing

from . import duration as _duration
from . import enumerate as _enumerate
from . import math as _math
from . import pitch as _pitch
from . import sequence as _sequence
from . import typedcollections as _typedcollections


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

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            \with
            {
                \override BarLine.stencil = ##f
                \override Glissando.thickness = 2
                \override SpanBar.stencil = ##f
                \override TimeSignature.stencil = ##f
            }
            <<
                \context PianoStaff = "Piano_Staff"
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

    """

    __slots__ = (
        "_close_bracket",
        "_open_bracket",
        "_range_string",
        "_start_pitch",
        "_stop_pitch",
    )

    def __init__(self, range_string="[A0, C8]"):
        if isinstance(range_string, type(self)):
            range_string = range_string.range_string
        assert isinstance(range_string, str), repr(range_string)
        bundle = self._parse_range_string(range_string)
        assert isinstance(bundle.start_pitch, (_pitch.NamedPitch, type(None)))
        assert isinstance(bundle.stop_pitch, (_pitch.NamedPitch, type(None)))
        self._close_bracket = bundle.close_bracket
        self._open_bracket = bundle.open_bracket
        self._range_string = bundle.range_string
        self._start_pitch = bundle.start_pitch
        self._stop_pitch = bundle.stop_pitch

    def __contains__(self, argument) -> bool:
        """
        Is true when pitch range contains ``argument``.

        ..  container:: example

            Closed / closed range:

            >>> range_ = abjad.PitchRange("[A0, C8]")

            >>> "C0" in range_
            False

            >>> "A0" in range_
            True

            >>> "C4" in range_
            True

            >>> "C8" in range_
            True

            >>> "C12" in range_
            False

        ..  container:: example

            Closed / open range:

            >>> range_ = abjad.PitchRange("[A0, C8)")

            >>> "C0" in range_
            False

            >>> "A0" in range_
            True

            >>> "C4" in range_
            True

            >>> "C8" in range_
            False

            >>> "C12" in range_
            False

        ..  container:: example

            Closed / infinite range:

            >>> range_ = abjad.PitchRange("[A0, +inf]")

            >>> "C0" in range_
            False

            >>> "A0" in range_
            True

            >>> "C4" in range_
            True

            >>> "C8" in range_
            True

            >>> "C12" in range_
            True

        ..  container:: example

            Open / closed range:

            >>> range_ = abjad.PitchRange("(A0, C8]")

            >>> "C0" in range_
            False

            >>> "A0" in range_
            False

            >>> "C4" in range_
            True

            >>> "C8" in range_
            True

            >>> "C12" in range_
            False

        ..  container:: example

            Open / open range:

            >>> range_ = abjad.PitchRange("(A0, C8)")

            >>> "C0" in range_
            False

            >>> "A0" in range_
            False

            >>> "C4" in range_
            True

            >>> "C8" in range_
            False

            >>> "C12" in range_
            False

        ..  container:: example

            Infinite / closed range:

            >>> range_ = abjad.PitchRange("[-inf, C8]")

            >>> "C0" in range_
            True

            >>> "A0" in range_
            True

            >>> "C4" in range_
            True

            >>> "C8" in range_
            True

            >>> "C12" in range_
            False

        ..  container:: example

            Infinite / open range:

            >>> range_ = abjad.PitchRange("[-inf, C8)")

            >>> "C0" in range_
            True

            >>> "A0" in range_
            True

            >>> "C4" in range_
            True

            >>> "C8" in range_
            False

            >>> "C12" in range_
            False

        ..  container:: example

            Infinite / infinite range:

            >>> range_ = abjad.PitchRange("[-inf, +inf]")

            >>> "C0" in range_
            True

            >>> "A0" in range_
            True

            >>> "C4" in range_
            True

            >>> "C8" in range_
            True

            >>> "C12" in range_
            True

        ..  container:: example

            Raises exception when argument is not a named pitch or string:

            >>> -99 in range_
            Traceback (most recent call last):
                ...
            Exception: must be named pitch or string (not -99).

        """
        if isinstance(argument, (str, _pitch.NamedPitch)):
            pitch = _pitch.NamedPitch(argument)
            if self.start_pitch is None:
                start_pitch = _pitch.NamedPitch(-1000)
            else:
                start_pitch = _pitch.NamedPitch(self.start_pitch)
            if self.stop_pitch is None:
                stop_pitch = _pitch.NamedPitch(1000)
            else:
                stop_pitch = _pitch.NamedPitch(self.stop_pitch)
        else:
            raise Exception(f"must be named pitch or string (not {argument!r}).")
        if self._open_bracket == "[":
            if self._close_bracket == "]":
                return start_pitch <= pitch <= stop_pitch
            else:
                return start_pitch <= pitch < stop_pitch
        else:
            if self._close_bracket == "]":
                return start_pitch < pitch <= stop_pitch
            else:
                return start_pitch < pitch < stop_pitch

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a pitch range with ``range_string`` equal to this
        pitch range.

        ..  container:: example

            >>> range_1 = abjad.PitchRange("[A0, C4]")
            >>> range_2 = abjad.PitchRange("[A0, C4]")
            >>> range_3 = abjad.PitchRange("[A0, C8]")

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

        """
        if isinstance(argument, type(self)):
            return self.range_string == argument.range_string
        return False

    def __hash__(self) -> int:
        """
        Hashes pitch range.
        """
        return hash(repr(self))

    def __lt__(self, argument) -> bool:
        """
        Is true when start pitch of this pitch-range is less than start pitch of
        ``argument`` pitch range.

        ..  container:: example

            >>> range_1 = abjad.PitchRange("[A0, C4]")
            >>> range_2 = abjad.PitchRange("[A0, C4]")
            >>> range_3 = abjad.PitchRange("[A0, C8]")

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

        """
        assert isinstance(argument, type(self)), repr(argument)
        if self.start_pitch is None:
            self_start_pitch = _pitch.NamedPitch(-1000)
        else:
            self_start_pitch = _pitch.NamedPitch(self.start_pitch)
        if self.stop_pitch is None:
            self_stop_pitch = _pitch.NamedPitch(1000)
        else:
            self_stop_pitch = _pitch.NamedPitch(self.stop_pitch)
        if argument.start_pitch is None:
            argument_start_pitch = _pitch.NamedPitch(-1000)
        else:
            argument_start_pitch = _pitch.NamedPitch(argument.start_pitch)
        if argument.stop_pitch is None:
            argument_stop_pitch = _pitch.NamedPitch(1000)
        else:
            argument_stop_pitch = _pitch.NamedPitch(argument.stop_pitch)
        if self_start_pitch == argument_start_pitch:
            return self_stop_pitch < argument_stop_pitch
        return self_start_pitch < argument_start_pitch

    def __repr__(self) -> str:
        """
        Gets pitch range interpreter representation.
        """
        return f"{type(self).__name__}(range_string={self.range_string!r})"

    def _parse_range_string(self, range_string):
        assert isinstance(range_string, str), repr(range_string)
        range_string = range_string.replace("-inf", "-1000")
        range_string = range_string.replace("+inf", "1000")
        match = _pitch._range_string_regex.match(range_string)
        if match is None:
            raise ValueError(f"can not parse range string: {range_string!r}")
        group_dict = match.groupdict()
        open_bracket = group_dict["open_bracket"]
        start_pitch_string = group_dict["start_pitch"]
        stop_pitch_string = group_dict["stop_pitch"]
        close_bracket = group_dict["close_bracket"]
        if start_pitch_string == "-1000":
            start_pitch = None
            start_pitch_repr = "-inf"
        elif start_pitch_string.isnumeric() or start_pitch_string.startswith("-"):
            raise Exception(f"named pitches only (not {range_string!r}).")
        else:
            start_pitch = _pitch.NamedPitch(start_pitch_string)
            start_pitch_repr = start_pitch.get_name(locale="us")

        if stop_pitch_string == "1000":
            stop_pitch = None
            stop_pitch_repr = "+inf"
        elif stop_pitch_string.isnumeric() or stop_pitch_string.startswith("-"):
            raise Exception(f"named pitches only (not {range_string!r}).")
        else:
            stop_pitch = _pitch.NamedPitch(stop_pitch_string)
            stop_pitch_repr = stop_pitch.get_name(locale="us")
        start, stop = open_bracket, close_bracket
        normalized_range_string = f"{start}{start_pitch_repr}, {stop_pitch_repr}{stop}"
        return types.SimpleNamespace(
            close_bracket=close_bracket,
            open_bracket=open_bracket,
            range_string=normalized_range_string,
            start_pitch=start_pitch,
            stop_pitch=stop_pitch,
        )

    @property
    def range_string(self) -> str:
        """
        Gets range string of pitch range.

        ..  container:: example

            >>> abjad.PitchRange("[C3, C7]").range_string
            '[C3, C7]'

            >>> abjad.PitchRange("[-inf, C7]").range_string
            '[-inf, C7]'

            >>> abjad.PitchRange("[C3, +inf]").range_string
            '[C3, +inf]'

            >>> abjad.PitchRange("[-inf, +inf]").range_string
            '[-inf, +inf]'

        """
        return self._range_string

    @property
    def start_pitch(self) -> _pitch.NamedPitch | None:
        """
        Start pitch of pitch range.

        ..  container:: example

            >>> abjad.PitchRange("[C3, C7]").start_pitch
            NamedPitch('c')

            >>> abjad.PitchRange("[-inf, C7]").start_pitch is None
            True

        """
        return self._start_pitch

    @property
    def stop_pitch(self) -> _pitch.NamedPitch | None:
        """
        Stop pitch of pitch range.

        ..  container:: example

            >>> abjad.PitchRange("[C3, C7]").stop_pitch
            NamedPitch("c''''")

            >>> abjad.PitchRange("[C8, +inf]").stop_pitch is None
            True

        """
        return self._stop_pitch

    @staticmethod
    def from_octave(octave) -> "PitchRange":
        """
        Initializes pitch range from octave.

        ..  container:: example

            >>> abjad.PitchRange.from_octave(5)
            PitchRange(range_string='[C5, C6)')

        """
        octave = _pitch.Octave(octave)
        return PitchRange(f"[C{octave.number}, C{octave.number + 1})")

    def voice_pitch_class(self, pitch_class):
        """
        Voices ``pitch_class``.

        ..  container:: example

            Voices C three times:

            >>> pitch_range = abjad.PitchRange("[C4, C6]")
            >>> pitch_range.voice_pitch_class("c")
            (NamedPitch("c'"), NamedPitch("c''"), NamedPitch("c'''"))

            Voices B two times:

            >>> pitch_range = abjad.PitchRange("[C4, C6]")
            >>> pitch_range.voice_pitch_class("b")
            (NamedPitch("b'"), NamedPitch("b''"))

            Returns empty because B can not voice:

            >>> pitch_range = abjad.PitchRange("[C4, A4)")
            >>> pitch_range.voice_pitch_class("b")
            ()

        """
        named_pitch_class = _pitch.NamedPitchClass(pitch_class)
        pair = (named_pitch_class.name, self.start_pitch.octave.number)
        named_pitch = _pitch.NamedPitch(pair)
        result = []
        while named_pitch <= self.stop_pitch:
            if named_pitch in self:
                result.append(named_pitch)
            named_pitch += 12
        return tuple(result)


@dataclasses.dataclass(slots=True)
class Segment(_typedcollections.TypedTuple):
    """
    Abstract segment.
    """

    def __post_init__(self):
        prototype = (collections.abc.Iterator, types.GeneratorType)
        if isinstance(self.items, str):
            self.items = self.items.split()
        elif isinstance(self.items, prototype):
            self.items = [_ for _ in self.items]
        if self.item_class is None:
            self.item_class = self._named_item_class
            if self.items is not None:
                if isinstance(
                    self.items, _typedcollections.TypedCollection
                ) and issubclass(self.items.item_class, self._parent_item_class):
                    self.item_class = self.items.item_class
                elif len(self.items):
                    if isinstance(self.items, collections.abc.Set):
                        self.items = tuple(self.items)
                    if isinstance(self.items[0], str):
                        self.item_class = self._named_item_class
                    elif isinstance(self.items[0], (int, float)):
                        self.item_class = self._numbered_item_class
                    elif isinstance(self.items[0], self._parent_item_class):
                        self.item_class = type(self.items[0])
        if isinstance(self.item_class, str):
            abjad = importlib.import_module("abjad")
            globals_ = {"abjad": abjad}
            globals_.update(abjad.__dict__.copy())
            self.item_class = eval(self.item_class, globals_)
        assert issubclass(self.item_class, self._parent_item_class)
        # _typedcollections.TypedTuple.__init__(self, items=items, item_class=item_class)
        _typedcollections.TypedTuple.__post_init__(self)

    def __repr__(self):
        """
        Gets repr.
        """
        item_strings = [str(_) for _ in self.items]
        return f"{type(self).__name__}(items={item_strings}, item_class=abjad.{self.item_class.__name__})"

    def __str__(self) -> str:
        """
        Gets string representation of segment.
        """
        items = [str(_) for _ in self]
        string = ", ".join(items)
        return f"<{string}>"

    def _coerce_item(self, item):
        return self.item_class(item)

    def _get_padded_string(self, width=2):
        strings = []
        for item in self:
            string = f"{item!s:>{width}}"
            strings.append(string)
        string = ", ".join(strings)
        return f"<{string}>"


@dataclasses.dataclass(slots=True)
class IntervalClassSegment(Segment):
    """
    Interval-class segment.

    ..  container:: example

        >>> intervals = "m2 M10 -aug4 P5"
        >>> abjad.IntervalClassSegment(intervals)
        IntervalClassSegment(items=(NamedIntervalClass('+m2'), NamedIntervalClass('+M3'), NamedIntervalClass('-A4'), NamedIntervalClass('+P5')), item_class=<class 'abjad.pitch.NamedIntervalClass'>)

        >>> intervals = "P4 P5 P11 P12"
        >>> abjad.IntervalClassSegment(intervals)
        IntervalClassSegment(items=(NamedIntervalClass('+P4'), NamedIntervalClass('+P5'), NamedIntervalClass('+P4'), NamedIntervalClass('+P5')), item_class=<class 'abjad.pitch.NamedIntervalClass'>)

    """

    @property
    def _named_item_class(self):
        return _pitch.NamedIntervalClass

    @property
    def _numbered_item_class(self):
        return _pitch.NumberedIntervalClass

    @property
    def _parent_item_class(self):
        return _pitch.IntervalClass

    @property
    def is_tertian(self) -> bool:
        """
        Is true when all named interval-classes in segment are tertian.

        ..  container:: example

            >>> interval_class_segment = abjad.IntervalClassSegment(
            ...     items=[("major", 3), ("minor", 6), ("major", 6)],
            ...     item_class=abjad.NamedIntervalClass,
            ... )
            >>> interval_class_segment.is_tertian
            True

        """
        inversion_equivalent_interval_class_segment = dataclasses.replace(
            self, item_class=_pitch.NamedInversionEquivalentIntervalClass
        )
        for interval in inversion_equivalent_interval_class_segment:
            if not interval.number == 3:
                return False
        return True

    @classmethod
    def from_pitches(class_, pitches, item_class=None) -> "IntervalClassSegment":
        """
        Initializes interval-class segment from ``pitches``.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> pitches = abjad.iterate.pitches([staff_1, staff_2])
            >>> segment = abjad.IntervalClassSegment.from_pitches(pitches)
            >>> str(segment)
            '<-M2, -M3, -m3, +m7, +M7, -P5>'

        """
        pitch_segment = PitchSegment.from_pitches(pitches)
        pitches = [_ for _ in pitch_segment]
        intervals = _math.difference_series(pitches)
        return class_(items=intervals, item_class=item_class)

    def has_duplicates(self) -> bool:
        """
        Is true when segment contains duplicates.

        ..  container:: example

            >>> intervals = "m2 M3 -aug4 m2 P5"
            >>> segment = abjad.IntervalClassSegment(intervals)
            >>> segment.has_duplicates()
            True

            >>> intervals = "M3 -aug4 m2 P5"
            >>> segment = abjad.IntervalClassSegment(intervals)
            >>> segment.has_duplicates()
            False

        """
        return len(set(self)) < len(self)


@dataclasses.dataclass(slots=True)
class IntervalSegment(Segment):
    """
    Interval segment.

    ..  container:: example

        >>> intervals = "m2 M10 -aug4 P5"
        >>> abjad.IntervalSegment(intervals)
        IntervalSegment(items=(NamedInterval('+m2'), NamedInterval('+M10'), NamedInterval('-A4'), NamedInterval('+P5')), item_class=<class 'abjad.pitch.NamedInterval'>)

        >>> pitch_segment = abjad.PitchSegment("c d e f g a b c'")
        >>> abjad.IntervalSegment(pitch_segment)
        IntervalSegment(items=(NamedInterval('+M2'), NamedInterval('+M2'), NamedInterval('+m2'), NamedInterval('+M2'), NamedInterval('+M2'), NamedInterval('+M2'), NamedInterval('+m2')), item_class=<class 'abjad.pitch.NamedInterval'>)

    """

    def __post_init__(self):
        if isinstance(self.items, PitchSegment):
            intervals = []
            for one, two in _sequence.nwise(self.items):
                intervals.append(one - two)
            self.items = intervals
        Segment.__post_init__(self)

    @property
    def _named_item_class(self):
        return _pitch.NamedInterval

    @property
    def _numbered_item_class(self):
        return _pitch.NumberedInterval

    @property
    def _parent_item_class(self):
        return _pitch.Interval

    @property
    def slope(self):
        """
        Gets slope of interval segment.

        ..  container:: example

            The slope of a interval segment is the sum of its
            intervals divided by its length:

            >>> abjad.IntervalSegment([1, 2]).slope
            Multiplier(3, 2)

        Returns multiplier.
        """
        result = sum([x.number for x in self]) / len(self)
        return _duration.Multiplier.from_float(result)

    @property
    def spread(self):
        """
        Gets spread of interval segment.

        ..  container:: example

            The maximum interval spanned by any combination of
            the intervals within a numbered interval segment.

            >>> abjad.IntervalSegment([1, 2, -3, 1, -2, 1]).spread
            NumberedInterval(4)

            >>> abjad.IntervalSegment([1, 1, 1, 2, -3, -2]).spread
            NumberedInterval(5)

        Returns numbered interval.
        """
        current = maximum = minimum = 0
        for x in self:
            current += float(x.number)
            if maximum < current:
                maximum = current
            if current < minimum:
                minimum = current
        return _pitch.NumberedInterval(maximum - minimum)

    @classmethod
    def from_pitches(class_, pitches, item_class=None) -> "IntervalSegment":
        """
        Makes interval segment from ``pitches``.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
            >>> pitches = abjad.iterate.pitches(staff)
            >>> abjad.IntervalSegment.from_pitches(
            ...     pitches,
            ...     item_class=abjad.NumberedInterval,
            ... )
            IntervalSegment(items=(NumberedInterval(2), NumberedInterval(2), NumberedInterval(1), NumberedInterval(2), NumberedInterval(2), NumberedInterval(2), NumberedInterval(1)), item_class=<class 'abjad.pitch.NumberedInterval'>)

        """
        pitch_segment = PitchSegment.from_pitches(pitches)
        pitches = [_ for _ in pitch_segment]
        intervals = (-x for x in _math.difference_series(pitches))
        return class_(items=intervals, item_class=item_class)

    def has_duplicates(self) -> bool:
        """
        Is true if segment has duplicate items.

        ..  container:: example

            >>> intervals = "m2 M3 -aug4 m2 P5"
            >>> segment = abjad.IntervalSegment(intervals)
            >>> segment.has_duplicates()
            True

            >>> intervals = "M3 -aug4 m2 P5"
            >>> segment = abjad.IntervalSegment(intervals)
            >>> segment.has_duplicates()
            False

        """
        return len(set(self)) < len(self)

    def rotate(self, n=0):
        """
        Rotates interval segment by index ``n``.

        Returns new interval segment.
        """
        return dataclasses.replace(self, self[-n:] + self[:-n])


@dataclasses.dataclass(slots=True)
class PitchClassSegment(Segment):
    r"""
    Pitch-class segment.

    ..  container:: example

        Initializes segment with numbered pitch-classes:

        >>> items = [-2, -1.5, 6, 7, -1.5, 7]
        >>> segment = abjad.PitchClassSegment(items=items)
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> voice = lilypond_file["Voice"]
            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                bf'8
                bqf'8
                fs'8
                g'8
                bqf'8
                g'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }

    ..  container:: example

        Initializes segment with named pitch-classes:

        >>> items = ["c", "ef", "bqs,", "d"]
        >>> segment = abjad.PitchClassSegment(
        ...     items=items,
        ...     item_class=abjad.NamedPitchClass,
        ... )
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> voice = lilypond_file["Voice"]
            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                c'8
                ef'8
                bqs'8
                d'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }

    """

    def __post_init__(self):
        if not self.items and not self.item_class:
            self.item_class = self._named_item_class
        Segment.__post_init__(self)

    def __add__(self, argument) -> "PitchClassSegment":
        r"""
        Adds ``argument`` to segment.

        ..  container:: example

            Example segments:

            >>> pitch_numbers = [-2, -1.5, 6, 7, -1.5, 7]
            >>> abjad.PitchClassSegment(items=pitch_numbers)
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> J = abjad.PitchClassSegment(items=pitch_numbers)
            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> pitch_names = ["c", "ef", "bqs,", "d"]
            >>> abjad.PitchClassSegment(items=pitch_names)
            PitchClassSegment(items="c ef bqs d", item_class=NamedPitchClass)

            >>> K = abjad.PitchClassSegment(items=pitch_names)
            >>> lilypond_file = abjad.illustrate(K)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Adds J and K:

            >>> J + K
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7, 0, 3, 11.5, 2], item_class=NumberedPitchClass)

            >>> segment = J + K
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    c'8
                    ef'8
                    bqs'8
                    d'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Adds J repeatedly:

            >>> J + J + J
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> segment = J + J + J
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Adds transformed segments:

            >>> J.rotate(n=1) + K.rotate(n=2)
            PitchClassSegment(items=[7, 10, 10.5, 6, 7, 10.5, 11.5, 2, 0, 3], item_class=NumberedPitchClass)

            >>> segment = J.rotate(n=1) + K.rotate(n=2)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    g'8
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    bqs'8
                    d'8
                    c'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Reverses result:

            >>> segment = J.rotate(n=1) + K.rotate(n=2)
            >>> segment.retrograde()
            PitchClassSegment(items=[3, 0, 2, 11.5, 10.5, 7, 6, 10.5, 10, 7], item_class=NumberedPitchClass)

            >>> segment = segment.retrograde()
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    ef'8
                    c'8
                    d'8
                    bqs'8
                    bqf'8
                    g'8
                    fs'8
                    bqf'8
                    bf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        argument = type(self)(items=argument)
        items = self.items + argument.items
        return type(self)(items=items)

    def __contains__(self, argument) -> bool:
        r"""
        Is true when pitch-class segment contains ``argument``.

        ..  container:: example

            Example segments:

            >>> pitch_numbers = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=pitch_numbers)
            >>> segment
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> abjad.NamedPitch("bf") in segment
            True

            >>> abjad.NamedPitch("cs") in segment
            False

            >>> "bf" in segment
            True

            >>> "cs" in segment
            False

            >>> 10 in segment
            True

            >>> 13 in segment
            False

        Returns true or false.
        """
        return Segment.__contains__(self, argument)

    def __getitem__(self, argument):
        r"""
        Gets ``argument`` from segment.

        ..  container:: example

            Example segment:

            >>> pitch_numbers = [-2, -1.5, 6, 7, -1.5, 7]
            >>> abjad.PitchClassSegment(items=pitch_numbers)
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> J = abjad.PitchClassSegment(items=pitch_numbers)
            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Gets item at nonnegative index:

            >>> J[0]
            NumberedPitchClass(10)

        ..  container:: example

            Gets item at negative index:

            >>> J[-1]
            NumberedPitchClass(7)

        ..  container:: example

            Gets slice:

            >>> J[:4]
            PitchClassSegment(items=[10, 10.5, 6, 7], item_class=NumberedPitchClass)

            >>> segment = J[:4]
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Gets retrograde of slice:

            >>> J[:4].retrograde()
            PitchClassSegment(items=[7, 6, 10.5, 10], item_class=NumberedPitchClass)

            >>> segment = J[:4].retrograde()
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    g'8
                    fs'8
                    bqf'8
                    bf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Gets slice of retrograde:

            >>> J.retrograde()[:4]
            PitchClassSegment(items=[7, 10.5, 7, 6], item_class=NumberedPitchClass)

            >>> segment = J.retrograde()[:4]
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    g'8
                    bqf'8
                    g'8
                    fs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns pitch-class or pitch-class segment:

            >>> isinstance(segment, abjad.PitchClassSegment)
            True

        """
        return Segment.__getitem__(self, argument)

    def __mul__(self, n) -> "PitchClassSegment":
        r"""
        Multiplies pitch-class segment by ``n``.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> 2 * abjad.PitchClassSegment(items=items)
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

        """
        return Segment.__mul__(self, n)

    def __repr__(self) -> str:
        r"""
        Gets interpreter representation.

        ..  container:: example

            Interpreter representation:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> abjad.PitchClassSegment(items=items)
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

        """
        if self.item_class is _pitch.NamedPitchClass:
            contents = " ".join([str(_) for _ in self])
            contents = '"' + contents + '"'
        else:
            contents = ", ".join([str(_) for _ in self])
            contents = "[" + contents + "]"
        return f"{type(self).__name__}(items={contents}, item_class={self.item_class.__name__})"

    def __rmul__(self, n) -> "PitchClassSegment":
        r"""
        Multiplies ``n`` by pitch-class segment.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> abjad.PitchClassSegment(items=items) * 2
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

        """
        return Segment.__rmul__(self, n)

    def __str__(self) -> str:
        r"""
        Gets string representation of pitch-class segment.

        ..  container::

            >>> segment = abjad.PitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])
            >>> str(segment)
            'PC<10, 10.5, 6, 7, 10.5, 7>'

            Gets string represenation of named pitch class:

            >>> segment = abjad.PitchClassSegment(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NamedPitchClass,
            ... )
            >>> str(segment)
            'PC<bf bqf fs g bqf g>'

        """
        items = [str(_) for _ in self]
        separator = " "
        if self.item_class is _pitch.NumberedPitchClass:
            separator = ", "
        return f"PC<{separator.join(items)}>"

    @property
    def _named_item_class(self):
        return _pitch.NamedPitchClass

    @property
    def _numbered_item_class(self):
        return _pitch.NumberedPitchClass

    @property
    def _parent_item_class(self):
        return _pitch.PitchClass

    def _get_padded_string(self, width=2):
        string = Segment._get_padded_string(self, width=width)
        return "PC<" + string[1:-1] + ">"

    def _is_equivalent_under_transposition(self, argument):
        if not isinstance(argument, type(self)):
            return False
        if not len(self) == len(argument):
            return False
        difference = -(
            _pitch.NamedPitch((argument[0].name, 4))
            - _pitch.NamedPitch((self[0].name, 4))
        )
        new_pitch_classes = (x + difference for x in self)
        new_pitch_classes = dataclasses.replace(self, items=new_pitch_classes)
        return argument == new_pitch_classes

    @staticmethod
    def _make_rotate_method_name(n=0):
        return "r"

    def _transpose_to_zero(self):
        numbers = [_.number for _ in self]
        first_number = self[0].number
        numbers = [pc.number - first_number for pc in self]
        pcs = [_ % 12 for _ in numbers]
        return type(self)(items=pcs, item_class=self.item_class)

    def count(self, item) -> int:
        """
        Counts ``item`` in segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Counts existing item in segment:

            >>> segment.count(-1.5)
            2

            Counts nonexisting item in segment:

            >>> segment.count("text")
            0

            Returns nonnegative integer:

            >>> isinstance(segment.count("text"), int)
            True

        """
        return Segment.count(self, item)

    @classmethod
    def from_pitches(class_, pitches, item_class=None) -> "PitchClassSegment":
        """
        Initializes pitch-class segment from ``pitches``.

        ..  container:: example

            Initializes from selection:

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> staff_group = abjad.StaffGroup([staff_1, staff_2])
            >>> abjad.show(staff_group) # doctest: +SKIP

            >>> pitches = abjad.iterate.pitches(staff_group)
            >>> segment = abjad.PitchClassSegment.from_pitches(pitches)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Returns pitch-class segment:

            >>> segment
            PitchClassSegment(items="c d fs a b c g", item_class=NamedPitchClass)

        """
        pitch_segment = PitchSegment.from_pitches(pitches)
        return class_(items=pitch_segment, item_class=item_class)

    def has_duplicates(self) -> bool:
        """
        Is true when segment contains duplicate items.

        ..  container:: example

            Has duplicates:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment.has_duplicates()
            True

            Has no duplicates:

            >>> items = "c d e f g a b"
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment.has_duplicates()
            False

        """
        return len(set(self)) < len(self)

    def index(self, item):
        """
        Gets index of ``item`` in segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Gets index of first item in segment:

            >>> segment.index(-2)
            0

            Gets index of second item in segment:

            >>> segment.index(-1.5)
            1

            Returns nonnegative integer:

            >>> isinstance(segment.index(-1.5), int)
            True

        """
        return Segment.index(self, item)

    def invert(self, axis=None) -> "PitchClassSegment":
        r"""
        Inverts segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Inverts segment:

            >>> J.invert()
            PitchClassSegment(items=[2, 1.5, 6, 5, 1.5, 5], item_class=NumberedPitchClass)

            >>> segment = J.invert()
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    d'8
                    dqf'8
                    fs'8
                    f'8
                    dqf'8
                    f'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            Inverts inversion of segment:

            >>> J.invert().invert()
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> segment = J.invert().invert()
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment == J
            True

        """
        items = [_.invert(axis=axis) for _ in self]
        return type(self)(items=items)

    def multiply(self, n=1) -> "PitchClassSegment":
        r"""
        Multiplies pitch-classes in segment by ``n``.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Multiplies pitch-classes in segment by 1:

            >>> J.multiply(n=1)
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> segment = J.multiply(n=1)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            Multiplies pitch-classes in segment by 5:

            >>> J.multiply(n=5)
            PitchClassSegment(items=[2, 4.5, 6, 11, 4.5, 11], item_class=NumberedPitchClass)

            >>> segment = J.multiply(n=5)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    d'8
                    eqs'8
                    fs'8
                    b'8
                    eqs'8
                    b'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            Multiplies pitch-classes in segment by 7:

            >>> J.multiply(n=7)
            PitchClassSegment(items=[10, 1.5, 6, 1, 1.5, 1], item_class=NumberedPitchClass)

            >>> segment = J.multiply(n=7)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    dqf'8
                    fs'8
                    cs'8
                    dqf'8
                    cs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            Multiplies pitch-classes in segment by 11:

            >>> segment = J.multiply(n=11)
            >>> segment
            PitchClassSegment(items=[2, 7.5, 6, 5, 7.5, 5], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    d'8
                    gqs'8
                    fs'8
                    f'8
                    gqs'8
                    f'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        items = [_pitch.NumberedPitchClass(_) for _ in self]
        items = [_.multiply(n) for _ in items]
        return type(self)(items=items)

    def permute(self, row=None) -> "PitchClassSegment":
        r"""
        Permutes segment by twelve-tone ``row``.

        ..  container:: example

            >>> abjad.PitchClassSegment([-2, -1, 6, 7, -1, 7])
            PitchClassSegment(items=[10, 11, 6, 7, 11, 7], item_class=NumberedPitchClass)

            >>> segment = abjad.PitchClassSegment([-2, -1, 6, 7, -1, 7])
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  doctest:

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    b'8
                    fs'8
                    g'8
                    b'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment.permute([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
            PitchClassSegment(items=[4, 11, 5, 3, 11, 3], item_class=NumberedPitchClass)

            >>> segment = segment.permute([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    e'8
                    b'8
                    f'8
                    ef'8
                    b'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        row = TwelveToneRow(items=row)
        items = row(self)
        return type(self)(items=items)

    def retrograde(self) -> "PitchClassSegment":
        r"""
        Gets retrograde of segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Gets retrograde of segment:

            >>> segment = J.retrograde()
            >>> segment
            PitchClassSegment(items=[7, 10.5, 7, 6, 10.5, 10], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    g'8
                    bqf'8
                    g'8
                    fs'8
                    bqf'8
                    bf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            Gets retrograde of retrograde of segment:

            >>> segment = J.retrograde().retrograde()
            >>> segment
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment == J
            True

        """
        return type(self)(items=reversed(self.items))

    def rotate(self, n=0) -> "PitchClassSegment":
        r"""
        Rotates segment by index ``n``.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Rotates segment to the right:

            >>> J.rotate(n=1)
            PitchClassSegment(items=[7, 10, 10.5, 6, 7, 10.5], item_class=NumberedPitchClass)

            >>> segment = J.rotate(n=1)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    g'8
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            Rotates segment to the left:

            >>> J.rotate(n=-1)
            PitchClassSegment(items=[10.5, 6, 7, 10.5, 7, 10], item_class=NumberedPitchClass)

            >>> segment = J.rotate(n=-1)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    bf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            Rotates segment by zero:

            >>> J.rotate(n=0)
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> segment = J.rotate(n=0)
            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment == J
            True

        """
        items = _sequence.rotate(self.items, n=n)
        return type(self)(items=items)

    def to_named_pitch_classes(self) -> "PitchClassSegment":
        r"""
        Changes to named pitch-classes.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> segment
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_named_pitch_classes()
            >>> segment
            PitchClassSegment(items="bf bqf fs g bqf g", item_class=NamedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(
            ...     items=items,
            ...     item_class=abjad.NamedPitchClass,
            ... )
            >>> segment
            PitchClassSegment(items="bf bqf fs g bqf g", item_class=NamedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_named_pitch_classes()
            >>> segment
            PitchClassSegment(items="bf bqf fs g bqf g", item_class=NamedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns new segment.
        """
        return type(self)(self, item_class=_pitch.NamedPitchClass)

    def to_named_pitches(self) -> "PitchSegment":
        r"""
        Changes to pitches.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> segment
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_named_pitches()
            >>> segment
            PitchSegment(items="bf' bqf' fs' g' bqf' g'", item_class=NamedPitch)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        bf'1 * 1/8
                        bqf'1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        bqf'1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(
            ...     items=items,
            ...     item_class=abjad.NamedPitchClass,
            ... )
            >>> segment
            PitchClassSegment(items="bf bqf fs g bqf g", item_class=NamedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_named_pitches()
            >>> segment
            PitchSegment(items="bf' bqf' fs' g' bqf' g'", item_class=NamedPitch)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        bf'1 * 1/8
                        bqf'1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        bqf'1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        """
        return PitchSegment(items=self.items, item_class=_pitch.NamedPitch)

    def to_numbered_pitch_classes(self) -> "PitchClassSegment":
        r"""
        Changes to numbered pitch-classes.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> segment
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_numbered_pitch_classes()
            >>> segment
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(
            ...     items=items,
            ...     item_class=abjad.NamedPitchClass,
            ... )
            >>> segment
            PitchClassSegment(items="bf bqf fs g bqf g", item_class=NamedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_numbered_pitch_classes()
            >>> segment
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns new segment.
        """
        return type(self)(self, item_class=_pitch.NumberedPitchClass)

    def to_numbered_pitches(self) -> "PitchSegment":
        r"""
        Changes to pitches.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> segment
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_numbered_pitches()
            >>> segment
            PitchSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitch)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        bf'1 * 1/8
                        bqf'1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        bqf'1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(
            ...     items=items,
            ...     item_class=abjad.NamedPitchClass,
            ... )
            >>> segment
            PitchClassSegment(items="bf bqf fs g bqf g", item_class=NamedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_numbered_pitches()
            >>> segment
            PitchSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitch)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        bf'1 * 1/8
                        bqf'1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        bqf'1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        """
        return PitchSegment(items=self.items, item_class=_pitch.NumberedPitch)

    def to_pitch_classes(self) -> "PitchClassSegment":
        r"""
        Changes to pitch-classes.

        ..  container:: example

            To numbered pitch-class segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> segment
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_pitch_classes()
            >>> segment
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            To named pitch-class segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(
            ...     items=items,
            ...     item_class=abjad.NamedPitchClass,
            ... )
            >>> segment
            PitchClassSegment(items="bf bqf fs g bqf g", item_class=NamedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_pitch_classes()
            >>> segment
            PitchClassSegment(items="bf bqf fs g bqf g", item_class=NamedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns new segment.
        """
        return type(self)(self)

    def to_pitches(self) -> "PitchSegment":
        r"""
        Changes to pitches.

        ..  container:: example

            To numbered pitch segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> segment
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_pitches()
            >>> segment
            PitchSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitch)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        bf'1 * 1/8
                        bqf'1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        bqf'1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        ..  container:: example

            To named pitch segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = abjad.PitchClassSegment(
            ...     items=items,
            ...     item_class=abjad.NamedPitchClass,
            ... )
            >>> segment
            PitchClassSegment(items="bf bqf fs g bqf g", item_class=NamedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment = segment.to_pitches()
            >>> segment
            PitchSegment(items="bf' bqf' fs' g' bqf' g'", item_class=NamedPitch)

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        bf'1 * 1/8
                        bqf'1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        bqf'1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        """
        class_ = _pitch.Pitch
        item_class = class_._to_pitch_item_class(self.item_class)
        return PitchSegment(items=self.items, item_class=item_class)

    def transpose(self, n=0) -> "PitchClassSegment":
        r"""
        Transposes segment by index ``n``.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Transposes segment by positive index:

            >>> J.transpose(n=13)
            PitchClassSegment(items=[11, 11.5, 7, 8, 11.5, 8], item_class=NumberedPitchClass)

            >>> segment = J.transpose(n=13)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    b'8
                    bqs'8
                    g'8
                    af'8
                    bqs'8
                    af'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Transposes segment by negative index:

            >>> J.transpose(n=-13)
            PitchClassSegment(items=[9, 9.5, 5, 6, 9.5, 6], item_class=NumberedPitchClass)

            >>> segment = J.transpose(n=-13)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    a'8
                    aqs'8
                    f'8
                    fs'8
                    aqs'8
                    fs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Transposes segment by zero index:

            >>> J.transpose(n=0)
            PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

            >>> segment = J.transpose(n=0)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment == J
            True

        """
        items = [_.transpose(n=n) for _ in self]
        return type(self)(items=items)

    def voice_horizontally(self, initial_octave=4) -> "PitchSegment":
        r"""
        Voices segment with each pitch as close to the previous pitch as possible.

        ..  todo:: Should be implemented somewhere else.

        ..  container:: example

            Voices horizontally:

            >>> items = "c b d e f g e b a c"
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> voiced_segment = segment.voice_horizontally()
            >>> lilypond_file = abjad.illustrate(voiced_segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                \with
                {
                    \override BarLine.stencil = ##f
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                }
                <<
                    \context PianoStaff = "Piano_Staff"
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            c'1 * 1/8
                            b1 * 1/8
                            d'1 * 1/8
                            e'1 * 1/8
                            f'1 * 1/8
                            g'1 * 1/8
                            e'1 * 1/8
                            b1 * 1/8
                            r1 * 1/8
                            c'1 * 1/8
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            a1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

        """
        initial_octave = _pitch.Octave(initial_octave)
        pitches = []
        if self:
            pitch_class = _pitch.NamedPitchClass(self[0])
            # pitch = _pitch.NamedPitch((pitch_class.name, initial_octave))
            pitch = _pitch.NamedPitch((pitch_class.name, initial_octave)).number
            pitches.append(pitch)
            for pitch_class in self[1:]:
                pitch_class = _pitch.NamedPitchClass(pitch_class)
                # pitch = _pitch.NamedPitch((pitch_class.name, initial_octave))
                pitch = _pitch.NamedPitch((pitch_class.name, initial_octave)).number
                # semitones = abs((pitch - pitches[-1]).semitones)
                semitones = abs((pitch - pitches[-1]))
                while 6 < semitones:
                    if pitch < pitches[-1]:
                        pitch += 12
                    else:
                        pitch -= 12
                    # semitones = abs((pitch - pitches[-1]).semitones)
                    semitones = abs((pitch - pitches[-1]))
                pitches.append(pitch)
        if self.item_class is _pitch.NamedPitchClass:
            segment = PitchSegment(items=pitches, item_class=_pitch.NamedPitch)
        else:
            segment = PitchSegment(items=pitches, item_class=_pitch.NumberedPitch)
        return segment

    def voice_vertically(self, initial_octave=4) -> "PitchSegment":
        r"""
        Voices segment with each pitch higher than the previous.

        ..  todo:: Should be implemented somewhere else.

        ..  container:: example

            Voices vertically:

            >>> string = "c' ef' g' bf' d'' f'' af''"
            >>> segment = abjad.PitchClassSegment(string)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> voiced_segment = segment.voice_vertically()
            >>> lilypond_file = abjad.illustrate(voiced_segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                \with
                {
                    \override BarLine.stencil = ##f
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                }
                <<
                    \context PianoStaff = "Piano_Staff"
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            c'1 * 1/8
                            ef'1 * 1/8
                            g'1 * 1/8
                            bf'1 * 1/8
                            d''1 * 1/8
                            f''1 * 1/8
                            af''1 * 1/8
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

        """
        initial_octave = _pitch.Octave(initial_octave)
        pitches = []
        if self:
            pitch_class = _pitch.NamedPitchClass(self[0])
            pitch = _pitch.NamedPitch((pitch_class.name, initial_octave))
            pitches.append(pitch)
            for pitch_class in self[1:]:
                pitch_class = _pitch.NamedPitchClass(pitch_class)
                pitch = _pitch.NamedPitch((pitch_class.name, initial_octave))
                while pitch < pitches[-1]:
                    pitch += 12
                pitches.append(pitch)
        if self.item_class is _pitch.NamedPitchClass:
            segment = PitchSegment(items=pitches, item_class=_pitch.NamedPitch)
        else:
            segment = PitchSegment(items=pitches, item_class=_pitch.NumberedPitch)
        return segment


@dataclasses.dataclass(slots=True)
class PitchSegment(Segment):
    r"""
    Pitch segment.

    ..  container:: example

        Numbered pitch segment:

        >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

        >>> str(segment)
        '<-2, -1.5, 6, 7, -1.5, 7>'

        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \clef "treble"
                    r1 * 1/8
                    r1 * 1/8
                    fs'1 * 1/8
                    g'1 * 1/8
                    r1 * 1/8
                    g'1 * 1/8
                }
                \context Staff = "Bass_Staff"
                {
                    \clef "bass"
                    bf1 * 1/8
                    bqf1 * 1/8
                    r1 * 1/8
                    r1 * 1/8
                    bqf1 * 1/8
                    r1 * 1/8
                }
            >>

    ..  container:: example

        Named pitch segment:

        >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

        >>> str(segment)
        "<bf, aqs fs' g' bqf g'>"

        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \clef "treble"
                    r1 * 1/8
                    r1 * 1/8
                    fs'1 * 1/8
                    g'1 * 1/8
                    r1 * 1/8
                    g'1 * 1/8
                }
                \context Staff = "Bass_Staff"
                {
                    \clef "bass"
                    bf,1 * 1/8
                    aqs1 * 1/8
                    r1 * 1/8
                    r1 * 1/8
                    bqf1 * 1/8
                    r1 * 1/8
                }
            >>

    ..  container:: example

        Built-in max() works:

        >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
        >>> max(segment)
        NumberedPitch(7)

        Built-in min() works:

        >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
        >>> min(segment)
        NumberedPitch(-2)

    """

    def __post_init__(self):
        if not self.items and not self.item_class:
            self.item_class = self._named_item_class
        Segment.__post_init__(self)

    def __contains__(self, argument):
        """
        Is true when pitch segment contains ``argument``.

        ..  container:: example

            Numbered pitch segment:

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> abjad.NamedPitch("fs") in segment
            False

            >>> 6 in segment
            True

            >>> abjad.NamedPitch("f") in segment
            False

            >>> 5 in segment
            False

        Returns true or false.
        """
        return Segment.__contains__(self, argument)

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        if self.item_class is _pitch.NamedPitch:
            contents = " ".join([str(_) for _ in self])
            contents = '"' + contents + '"'
        else:
            contents = ", ".join([str(_) for _ in self])
            contents = "[" + contents + "]"
        return f"{type(self).__name__}(items={contents}, item_class={self.item_class.__name__})"

    def __str__(self) -> str:
        """
        Gets pitch segment string.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> str(segment)
            '<-2, -1.5, 6, 7, -1.5, 7>'

        ..  container:: example

            >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

            >>> str(segment)
            "<bf, aqs fs' g' bqf g'>"

        """
        items = [str(_) for _ in self]
        separator = " "
        if self.item_class is _pitch.NumberedPitch:
            separator = ", "
        return f"<{separator.join(items)}>"

    @property
    def _named_item_class(self):
        return _pitch.NamedPitch

    @property
    def _numbered_item_class(self):
        return _pitch.NumberedPitch

    @property
    def _parent_item_class(self):
        return _pitch.Pitch

    def _is_equivalent_under_transposition(self, argument):
        if not isinstance(argument, type(self)):
            return False
        if not len(self) == len(argument):
            return False
        difference = -(
            _pitch.NamedPitch(argument[0], 4) - _pitch.NamedPitch(self[0], 4)
        )
        new_pitches = (x + difference for x in self)
        new_pitches = dataclasses.replace(self, items=new_pitches)
        return argument == new_pitches

    @property
    def hertz(self) -> list[float]:
        """
        Gets Hertz of pitches in segment.

        ..  container:: example

            >>> segment = abjad.PitchSegment("c e g b")
            >>> segment.hertz
            [130.81..., 164.81..., 195.99..., 246.94...]

        """
        return [_.hertz for _ in self]

    @property
    def inflection_point_count(self) -> int:
        r"""
        Gets segment inflection point count.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.inflection_point_count
            2

        """
        return len(self.local_minima) + len(self.local_maxima)

    @property
    def local_maxima(self):
        r"""
        Gets segment local maxima.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.local_maxima
            [NumberedPitch(7)]

        Returns list.
        """
        result = []
        if 3 <= len(self):
            for i in range(1, len(self) - 1):
                left, middle, right = self[i - 1], self[i], self[i + 1]
                if left < middle and right < middle:
                    result.append(middle)
        return result

    @property
    def local_minima(self):
        r"""
        Gets segment local minima.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.local_minima
            [NumberedPitch(-1.5)]

        Returns list.
        """
        result = []
        if 3 <= len(self):
            for i in range(1, len(self) - 1):
                left, middle, right = self[i - 1], self[i], self[i + 1]
                if middle < left and middle < right:
                    result.append(middle)
        return result

    @classmethod
    def from_pitches(class_, pitches, item_class=None) -> "PitchSegment":
        r"""
        Makes pitch segment from ``pitches``.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> pitches = abjad.iterate.pitches([staff_1, staff_2])
            >>> segment = abjad.PitchSegment.from_pitches(pitches)

            >>> str(segment)
            "<c' d' fs' a' b c g>"

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        c'1 * 1/8
                        d'1 * 1/8
                        fs'1 * 1/8
                        a'1 * 1/8
                        b1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        c1 * 1/8
                        g1 * 1/8
                    }
                >>

        """
        return class_(items=pitches, item_class=item_class)

    def has_duplicates(self) -> bool:
        """
        Is true when segment has duplicates.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
            >>> segment.has_duplicates()
            True

        ..  container:: example

            >>> segment = abjad.PitchSegment("c d e f g a b")
            >>> segment.has_duplicates()
            False

        """
        return len(set(self)) < len(self)

    def invert(self, axis=None) -> "PitchSegment":
        r"""
        Inverts pitch segment about ``axis``.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.invert(axis=0)

            >>> str(segment)
            '<2, 1.5, -6, -7, 1.5, -7>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        d'1 * 1/8
                        dqf'1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        dqf'1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        fs1 * 1/8
                        f1 * 1/8
                        r1 * 1/8
                        f1 * 1/8
                    }
                >>

        """
        items = [_.invert(axis=axis) for _ in self]
        return dataclasses.replace(self, items=items)

    def multiply(self, n=1) -> "PitchSegment":
        r"""
        Multiplies pitch segment by index ``n``.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.multiply(n=3)

            >>> str(segment)
            '<-6, -4.5, 18, 21, -4.5, 21>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs''1 * 1/8
                        a''1 * 1/8
                        r1 * 1/8
                        a''1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        fs1 * 1/8
                        gqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        gqs1 * 1/8
                        r1 * 1/8
                    }
                >>

        """
        items = [_.multiply(n=n) for _ in self]
        return dataclasses.replace(self, items=items)

    def retrograde(self) -> "PitchSegment":
        r"""
        Retrograde of pitch segment.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.retrograde()

            >>> str(segment)
            '<7, -1.5, 7, 6, -1.5, -2>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                        fs'1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        bf1 * 1/8
                    }
                >>

        """
        return dataclasses.replace(self, items=reversed(self))

    def rotate(self, n=0) -> "PitchSegment":
        r"""
        Rotates pitch segment by index ``n``.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.rotate(n=1)

            >>> str(segment)
            '<7, -2, -1.5, 6, 7, -1.5>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        g'1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                    }
                >>

        """
        rotated_pitches = _sequence.rotate(self.items, n=n)
        new_segment = dataclasses.replace(self, items=rotated_pitches)
        return new_segment

    def to_named_pitch_classes(self) -> "PitchClassSegment":
        r"""
        Changes to named pitch-classes.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_named_pitch_classes()

            >>> str(segment)
            'PC<bf bqf fs g bqf g>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        aqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_named_pitch_classes()

            >>> str(segment)
            'PC<bf aqs fs g bqf g>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    aqs'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        return PitchClassSegment(items=self.items, item_class=_pitch.NamedPitchClass)

    def to_named_pitches(self) -> "PitchSegment":
        r"""
        Changes to named pitches.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_named_pitches()

            >>> str(segment)
            "<bf bqf fs' g' bqf g'>"

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

        ..  container:: example

            To named pitch segment:

            >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        aqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_named_pitches()

            >>> str(segment)
            "<bf, aqs fs' g' bqf g'>"

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        aqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

        """
        return type(self)(items=self.items, item_class=_pitch.NamedPitch)

    def to_numbered_pitch_classes(self) -> "PitchClassSegment":
        r"""
        Changes to numbered pitch-classes.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_numbered_pitch_classes()

            >>> str(segment)
            'PC<10, 10.5, 6, 7, 10.5, 7>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        aqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_numbered_pitch_classes()

            >>> str(segment)
            'PC<10, 9.5, 6, 7, 10.5, 7>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    aqs'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        return PitchClassSegment(items=self.items, item_class=_pitch.NumberedPitchClass)

    def to_numbered_pitches(self) -> "PitchSegment":
        r"""
        Changes to numbered pitches.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_numbered_pitches()

            >>> str(segment)
            '<-2, -1.5, 6, 7, -1.5, 7>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

        ..  container:: example

            To named pitch segment:

            >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        aqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_numbered_pitches()

            >>> str(segment)
            '<-14, -2.5, 6, 7, -1.5, 7>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        aqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

        """
        return type(self)(items=self.items, item_class=_pitch.NumberedPitch)

    def to_pitch_classes(self) -> "PitchClassSegment":
        r"""
        Changes to pitch-classes.

        ..  container:: example

            To numbered pitch-class segment:

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_pitch_classes()

            >>> str(segment)
            'PC<10, 10.5, 6, 7, 10.5, 7>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            To named pitch-class segment:

            >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        aqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_pitch_classes()

            >>> str(segment)
            'PC<bf aqs fs g bqf g>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    aqs'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        class_ = _pitch.Pitch
        item_class = class_._to_pitch_class_item_class(self.item_class)
        return PitchClassSegment(items=self.items, item_class=item_class)

    def to_pitches(self) -> "PitchSegment":
        r"""
        Changes to pitches.

        ..  container:: example

            To numbered pitch segment:

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_pitches()

            >>> str(segment)
            '<-2, -1.5, 6, 7, -1.5, 7>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

        ..  container:: example

            To named pitch segment:

            >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        aqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_pitches()

            >>> str(segment)
            "<bf, aqs fs' g' bqf g'>"

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        aqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

        """
        return dataclasses.replace(self)

    def transpose(self, n=0) -> "PitchSegment":
        r"""
        Transposes pitch segment by index ``n``.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.transpose(n=11)

            >>> str(segment)
            '<9, 9.5, 17, 18, 9.5, 18>'

            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        a'1 * 1/8
                        aqs'1 * 1/8
                        f''1 * 1/8
                        fs''1 * 1/8
                        aqs'1 * 1/8
                        fs''1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        """
        items = [_.transpose(n=n) for _ in self]
        return dataclasses.replace(self, items=items)


@dataclasses.dataclass(slots=True)
class TwelveToneRow(PitchClassSegment):
    """
    Twelve-tone row.

    ..  container:: example

        Initializes from defaults:

        >>> row = abjad.TwelveToneRow()
        >>> lilypond_file = abjad.illustrate(row)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        Initializes from integers:

        >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
        >>> row = abjad.TwelveToneRow(numbers)
        >>> lilypond_file = abjad.illustrate(row)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        Interpreter representation:

        >>> row
        TwelveToneRow(items=(NumberedPitchClass(1), NumberedPitchClass(11), NumberedPitchClass(9), NumberedPitchClass(3), NumberedPitchClass(6), NumberedPitchClass(7), NumberedPitchClass(5), NumberedPitchClass(4), NumberedPitchClass(10), NumberedPitchClass(2), NumberedPitchClass(8), NumberedPitchClass(0)), item_class=<class 'abjad.pitch.NumberedPitchClass'>)

    """

    items: typing.Any = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)

    def __post_init__(self):
        assert self.items is not None
        PitchClassSegment.__post_init__(self)
        self._validate_pitch_classes(self)

    def __call__(self, pitch_classes):
        r"""
        Calls row on ``pitch_classes``.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Permutes pitch-classes:

            >>> row([abjad.NumberedPitchClass(2)])
            [NumberedPitchClass(9)]

            >>> row([abjad.NumberedPitchClass(3)])
            [NumberedPitchClass(3)]

            >>> row([abjad.NumberedPitchClass(4)])
            [NumberedPitchClass(6)]

        ..  container:: example

            Permutes pitch-class segment:

            >>> items = [-2, -1, 6, 7, -1, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment_ = row(segment)
            >>> lilypond_file = abjad.illustrate(segment_)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    af'8
                    c'8
                    f'8
                    e'8
                    c'8
                    e'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Permutes row:

            >>> numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            >>> row_2 = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row_2)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> row_3 = row(row_2)
            >>> lilypond_file = abjad.illustrate(row_3)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Permutes row:

            >>> numbers = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
            >>> row_2 = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row_2)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    b'8
                    bf'8
                    a'8
                    af'8
                    g'8
                    fs'8
                    f'8
                    e'8
                    ef'8
                    d'8
                    cs'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> row_3 = row(row_2)
            >>> lilypond_file = abjad.illustrate(row_3)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    c'8
                    af'8
                    d'8
                    bf'8
                    e'8
                    f'8
                    g'8
                    fs'8
                    ef'8
                    a'8
                    b'8
                    cs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Permutes row:

            >>> numbers = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
            >>> row_2 = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row_2)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    bf'8
                    c'8
                    d'8
                    fs'8
                    af'8
                    g'8
                    f'8
                    ef'8
                    cs'8
                    a'8
                    e'8
                    b'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> row_3 = row(row_2)
            >>> lilypond_file = abjad.illustrate(row_3)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    af'8
                    cs'8
                    a'8
                    f'8
                    bf'8
                    e'8
                    g'8
                    ef'8
                    b'8
                    d'8
                    fs'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns permuted pitch-classes in object of type ``pitch_classes``.
        """
        new_pitch_classes = []
        for pitch_class in pitch_classes:
            pitch_class = _pitch.NumberedPitchClass(pitch_class)
            i = pitch_class.number
            new_pitch_class = self[i]
            new_pitch_classes.append(new_pitch_class)
        result = type(pitch_classes)(new_pitch_classes)
        return result

    def __getitem__(self, argument):
        r"""
        Gets item or slice identified by ``argument``.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Gets first hexachord:

            >>> lilypond_file = abjad.illustrate(row[:6])
            >>> abjad.show(lilypond_file) # doctest: +SKIP
            PitchClassSegment([0, 1, 11, 9, 3, 6])

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Gets second hexachord:

            >>> lilypond_file = abjad.illustrate(row[-6:])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Gets items in row:

            >>> row = abjad.TwelveToneRow()
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP


            >>> for item in row.items:
            ...     item
            ...
            NumberedPitchClass(0)
            NumberedPitchClass(1)
            NumberedPitchClass(2)
            NumberedPitchClass(3)
            NumberedPitchClass(4)
            NumberedPitchClass(5)
            NumberedPitchClass(6)
            NumberedPitchClass(7)
            NumberedPitchClass(8)
            NumberedPitchClass(9)
            NumberedPitchClass(10)
            NumberedPitchClass(11)

            Gets items in row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> for item in row.items:
            ...     item
            ...
            NumberedPitchClass(1)
            NumberedPitchClass(11)
            NumberedPitchClass(9)
            NumberedPitchClass(3)
            NumberedPitchClass(6)
            NumberedPitchClass(7)
            NumberedPitchClass(5)
            NumberedPitchClass(4)
            NumberedPitchClass(10)
            NumberedPitchClass(2)
            NumberedPitchClass(8)
            NumberedPitchClass(0)

        """
        item = self.items.__getitem__(argument)
        try:
            return PitchClassSegment(items=item, item_class=_pitch.NumberedPitchClass)
        except TypeError:
            return item

    def __mul__(self, argument) -> "PitchClassSegment":
        r"""
        Multiplies row by ``argument``.

        ..  container:: example

            Multiplies row:

            >>> row = abjad.TwelveToneRow()
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment = 2 * row
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment = 2 * row
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP


            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        return PitchClassSegment(self) * argument

    def __rmul__(self, argument) -> "PitchClassSegment":
        r"""
        Multiplies ``argument`` by row.

        ..  container:: example

            Multiplies integer by row:

            >>> row = abjad.TwelveToneRow()
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment = row * 2
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies integer by row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> segment = row * 2
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        return PitchClassSegment(self) * argument

    @property
    def _contents_string(self):
        return ", ".join([str(abs(pc)) for pc in self])

    @staticmethod
    def _validate_pitch_classes(pitch_classes):
        numbers = [pc.number for pc in pitch_classes]
        numbers.sort()
        if not numbers == list(range(12)):
            message = f"must contain all twelve pitch-classes: {pitch_classes!r}."
            raise ValueError(message)

    def count(self, item) -> int:
        """
        Counts ``item`` in row.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Counts pitch-class 11 in row:

            >>> row.count(11)
            1

        ..  container:: example

            Counts pitch-class 9 in row:

            >>> row.count(9)
            1

        ..  container:: example

            Counts string in row:

            >>> row.count("text")
            0

        """
        return PitchClassSegment.count(self, item)

    def has_duplicates(self) -> bool:
        """
        Is false for all rows.

        ..  container:: example

            Is false:

            >>> row = abjad.TwelveToneRow()
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> row.has_duplicates()
            False

        ..  container:: example

            Is false:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> row.has_duplicates()
            False

        Twelve-tone rows have no duplicates.
        """
        return PitchClassSegment.has_duplicates(self)

    def index(self, item):
        """
        Gets index of ``item`` in row.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Gets index of pitch-class 11:

            >>> row.index(11)
            1

        ..  container:: example

            Gets index of pitch-class 9:

            >>> row.index(9)
            2

        ..  container:: example

            Returns nonnegative integer less than 12:

            >>> isinstance(row.index(9), int)
            True

        """
        return PitchClassSegment.index(self, item)

    def invert(self, axis=None) -> "TwelveToneRow":
        r"""
        Inverts row about optional ``axis``.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Inverts row about first pitch-class when ``axis`` is none:

            >>> inversion = row.invert()
            >>> lilypond_file = abjad.illustrate(inversion)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    cs'8
                    ef'8
                    f'8
                    b'8
                    af'8
                    g'8
                    a'8
                    bf'8
                    e'8
                    c'8
                    fs'8
                    d'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            First pitch-classes are equal:

            >>> row[0] == inversion[0]
            True

        ..  container:: example

            Inverts row about pitch-class 1:

            >>> inversion = row.invert(axis=1)
            >>> lilypond_file = abjad.illustrate(inversion)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    cs'8
                    ef'8
                    f'8
                    b'8
                    af'8
                    g'8
                    a'8
                    bf'8
                    e'8
                    c'8
                    fs'8
                    d'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            Same result as above.

        ..  container:: example

            Inverts row about pitch-class 0:

            >>> inversion = row.invert(axis=0)
            >>> lilypond_file = abjad.illustrate(inversion)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    b'8
                    cs'8
                    ef'8
                    a'8
                    fs'8
                    f'8
                    g'8
                    af'8
                    d'8
                    bf'8
                    e'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Inverts row about pitch-class 5:

            >>> inversion = row.invert(axis=5)
            >>> lilypond_file = abjad.illustrate(inversion)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    a'8
                    b'8
                    cs'8
                    g'8
                    e'8
                    ef'8
                    f'8
                    fs'8
                    c'8
                    af'8
                    d'8
                    bf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        if axis is None:
            axis = self[0]
        items = [pc.invert(axis=axis) for pc in self]
        return dataclasses.replace(self, items=items)

    def multiply(self, n=1) -> "TwelveToneRow":
        r"""
        Multiplies pitch-classes in row by ``n``.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Multiplies pitch-classes in row by 5:

            >>> multiplication = row.multiply(n=5)
            >>> lilypond_file = abjad.illustrate(multiplication)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    f'8
                    g'8
                    a'8
                    ef'8
                    fs'8
                    b'8
                    cs'8
                    af'8
                    d'8
                    bf'8
                    e'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies pitch-classes in row by 7:

            >>> multiplication = row.multiply(n=7)
            >>> lilypond_file = abjad.illustrate(multiplication)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    g'8
                    f'8
                    ef'8
                    a'8
                    fs'8
                    cs'8
                    b'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies pitch-classes in row by 1:

            >>> multiplication = row.multiply(n=1)
            >>> lilypond_file = abjad.illustrate(multiplication)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        """
        return type(self)(PitchClassSegment.multiply(self, n=n))

    def retrograde(self) -> "TwelveToneRow":
        r"""
        Gets retrograde of row.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Gets retrograde of row:

            >>> retrograde = row.retrograde()
            >>> lilypond_file = abjad.illustrate(retrograde)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    c'8
                    af'8
                    d'8
                    bf'8
                    e'8
                    f'8
                    g'8
                    fs'8
                    ef'8
                    a'8
                    b'8
                    cs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Gets retrograde of retrograde of row:

            >>> retrograde = row.retrograde().retrograde()
            >>> lilypond_file = abjad.illustrate(retrograde)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> retrograde == row
            True

        """
        return type(self)(PitchClassSegment.retrograde(self))

    def rotate(self, n=0) -> "TwelveToneRow":
        r"""
        Rotates row by index ``n``.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Rotates row to the right:

            >>> rotation = row.rotate(n=1)
            >>> lilypond_file = abjad.illustrate(rotation)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    c'8
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Rotates row to the left:

            >>> rotation = row.rotate(n=-1)
            >>> lilypond_file = abjad.illustrate(rotation)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    cs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Rotates row by zero:

            >>> rotation = row.rotate(n=0)
            >>> lilypond_file = abjad.illustrate(rotation)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> rotation == row
            True

        """
        return type(self)(PitchClassSegment.rotate(self, n=n))

    def transpose(self, n=0) -> "TwelveToneRow":
        r"""
        Transposes row by index ``n``.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> lilypond_file = abjad.illustrate(row)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Transposes row by positive index:

            >>> transposition = row.transpose(n=13)
            >>> lilypond_file = abjad.illustrate(transposition)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    d'8
                    c'8
                    bf'8
                    e'8
                    g'8
                    af'8
                    fs'8
                    f'8
                    b'8
                    ef'8
                    a'8
                    cs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Transposes row by negative index:

            >>> transposition = row.transpose(n=-13)
            >>> lilypond_file = abjad.illustrate(transposition)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    c'8
                    bf'8
                    af'8
                    d'8
                    f'8
                    fs'8
                    e'8
                    ef'8
                    a'8
                    cs'8
                    g'8
                    b'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Transposes row by zero index:

            >>> transposition = row.transpose(n=0)
            >>> lilypond_file = abjad.illustrate(transposition)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> transposition == row
            True

        """
        return type(self)(PitchClassSegment.transpose(self, n=n))


@dataclasses.dataclass(slots=True)
class Set(_typedcollections.TypedFrozenset):
    """
    Abstract set.
    """

    def __post_init__(self):
        if isinstance(self.items, str):
            self.items = self.items.split()
        elif isinstance(self.items, (collections.abc.Iterator, types.GeneratorType)):
            self.items = [item for item in self.items]
        if self.item_class is None:
            self.item_class = self._named_item_class
            if self.items is not None:
                if isinstance(
                    self.items, _typedcollections.TypedCollection
                ) and issubclass(self.items.item_class, self._parent_item_class):
                    self.item_class = self.items.item_class
                elif len(self.items):
                    if isinstance(self.items, collections.abc.Set):
                        self.items = tuple(self.items)
                    if isinstance(self.items[0], str):
                        self.item_class = self._named_item_class
                    elif isinstance(self.items[0], (int, float)):
                        self.item_class = self._numbered_item_class
                    elif isinstance(self.items[0], self._parent_item_class):
                        self.item_class = type(self.items[0])
        assert issubclass(self.item_class, self._parent_item_class)
        _typedcollections.TypedFrozenset.__post_init__(self)

    def __repr__(self):
        """
        Gets repr of set.
        """
        return f"{type(self).__name__}(items={self._get_sorted_repr_items()}, item_class=abjad.{self.item_class.__name__})"

    def _sort_self(self):
        return tuple(self)

    @property
    def cardinality(self):
        """
        Gets cardinality of set.

        Defined equal to length of set.

        Returns nonnegative integer.
        """
        return len(self)


@dataclasses.dataclass(slots=True)
class IntervalClassSet(Set):
    """
    Interval-class set.
    """

    def __post_init__(self):
        prototype = (
            PitchClassSegment,
            PitchSegment,
            PitchClassSet,
            PitchSet,
        )
        if isinstance(self.items, prototype):
            self.items = list(self.items)
            pairs = _enumerate.yield_pairs(self.items)
            self.items = [second - first for first, second in pairs]
        Set.__post_init__(self)

    @property
    def _named_item_class(self):
        return _pitch.NamedIntervalClass

    @property
    def _numbered_item_class(self):
        return _pitch.NumberedIntervalClass

    @property
    def _parent_item_class(self):
        return _pitch.IntervalClass

    @classmethod
    def from_pitches(class_, pitches, item_class=None) -> "IntervalClassSet":
        r"""
        Initializes interval set from ``pitches``.

        ..  container:: example

            ::

                >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
                >>> staff_2 = abjad.Staff("c4. r8 g2")
                >>> staff_group = abjad.StaffGroup([staff_1, staff_2])
                >>> abjad.show(staff_group) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \new StaffGroup
                <<
                    \new Staff
                    {
                        c'4
                        <d' fs' a'>4
                        b2
                    }
                    \new Staff
                    {
                        c4.
                        r8
                        g2
                    }
                >>

            ::

                >>> pitches = abjad.iterate.pitches(staff_group)
                >>> interval_classes = abjad.IntervalClassSet.from_pitches(pitches)
                >>> for interval_class in sorted(interval_classes):
                ...     interval_class
                ...
                NamedIntervalClass('-M6')
                NamedIntervalClass('-P5')
                NamedIntervalClass('-A4')
                NamedIntervalClass('-M3')
                NamedIntervalClass('-m3')
                NamedIntervalClass('-M2')
                NamedIntervalClass('+m2')
                NamedIntervalClass('+M2')
                NamedIntervalClass('+m3')
                NamedIntervalClass('+M3')
                NamedIntervalClass('+P4')
                NamedIntervalClass('+A4')
                NamedIntervalClass('+P5')
                NamedIntervalClass('+M6')
                NamedIntervalClass('+m7')
                NamedIntervalClass('+M7')
                NamedIntervalClass('+P8')

        """
        interval_set = IntervalSet.from_pitches(pitches)
        return class_(items=interval_set, item_class=item_class)


@dataclasses.dataclass(slots=True)
class IntervalSet(Set):
    """
    Interval set.
    """

    def __post_init__(self):
        prototype = (
            PitchClassSegment,
            PitchClassSet,
            PitchSegment,
            PitchSet,
        )
        if isinstance(self.items, prototype):
            self.items = list(self.items)
            pairs = _enumerate.yield_pairs(self.items)
            self.items = [second - first for first, second in pairs]
        Set.__post_init__(self)

    @property
    def _named_item_class(self):
        return _pitch.NamedInterval

    @property
    def _numbered_item_class(self):
        return _pitch.NumberedInterval

    @property
    def _parent_item_class(self):
        return _pitch.Interval

    @classmethod
    def from_pitches(class_, pitches, item_class=None) -> "IntervalSet":
        """
        Initializes interval set from ``pitches``.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> pitches = abjad.iterate.pitches([staff_1, staff_2])
            >>> intervals = abjad.IntervalSet.from_pitches(pitches)
            >>> for interval in sorted(intervals):
            ...     interval
            ...
            NamedInterval('-M6')
            NamedInterval('-P5')
            NamedInterval('-A4')
            NamedInterval('-M3')
            NamedInterval('-m3')
            NamedInterval('-M2')
            NamedInterval('+m2')
            NamedInterval('+m3')
            NamedInterval('+M3')
            NamedInterval('+P4')
            NamedInterval('+P5')
            NamedInterval('+m7')
            NamedInterval('+M7')
            NamedInterval('+P8')
            NamedInterval('+M9')
            NamedInterval('+A11')
            NamedInterval('+M13')

        """
        pitch_segment = PitchSegment.from_pitches(pitches)
        pairs = _enumerate.yield_pairs(pitch_segment)
        intervals = [second - first for first, second in pairs]
        return class_(items=intervals, item_class=item_class)


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class PitchClassSet(Set):
    """
    Pitch-class set.

    ..  container:: example

        Initializes numbered pitch-class set:

        >>> numbered_pitch_class_set = abjad.PitchClassSet(
        ...     items=[-2, -1.5, 6, 7, -1.5, 7],
        ...     item_class=abjad.NumberedPitchClass,
        ... )
        >>> numbered_pitch_class_set
        PitchClassSet(items=[6, 7, 10, 10.5], item_class=abjad.NumberedPitchClass)

    ..  container:: example

        Initializes named pitch-class set:

        >>> named_pitch_class_set = abjad.PitchClassSet(
        ...     items=["c", "ef", "bqs,", "d"],
        ...     item_class=abjad.NamedPitchClass,
        ... )
        >>> named_pitch_class_set
        PitchClassSet(items=['c', 'd', 'ef', 'bqs'], item_class=abjad.NamedPitchClass)

    """

    def __repr__(self):
        """
        Gets repr of pitch-class set.
        """
        return f"{type(self).__name__}(items={self._get_sorted_repr_items()}, item_class=abjad.{self.item_class.__name__})"

    def __contains__(self, argument):
        """
        Is true when pitch-class set contains ``argument``.

        ..  container:: example

            Initializes numbered pitch-class set:

            >>> set_ = abjad.PitchClassSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitchClass,
            ... )
            >>> set_
            PitchClassSet(items=[6, 7, 10, 10.5], item_class=abjad.NumberedPitchClass)

            >>> abjad.NamedPitch("fs") in set_
            True

            >>> abjad.NamedPitch("f") in set_
            False

            >>> 6 in set_
            True

            >>> 5 in set_
            False

        Returns true or false.
        """
        return Set.__contains__(self, argument)

    def __str__(self) -> str:
        """
        Gets string representation of pitch-class set.

        ..  container:: example

            Gets string of set sorted at initialization:

            >>> pc_set = abjad.PitchClassSet([6, 7, 10, 10.5])
            >>> str(pc_set)
            'PC{6, 7, 10, 10.5}'

        ..  container:: example

            Gets string of set not sorted at initialization:

            >>> pc_set = abjad.PitchClassSet([10.5, 10, 7, 6])
            >>> str(pc_set)
            'PC{6, 7, 10, 10.5}'

        """
        items = [str(_) for _ in sorted(self)]
        separator = " "
        if self.item_class is _pitch.NumberedPitchClass:
            separator = ", "
        return f"PC{{{separator.join(items)}}}"

    @property
    def _named_item_class(self):
        return _pitch.NamedPitchClass

    @property
    def _numbered_item_class(self):
        return _pitch.NumberedPitchClass

    @property
    def _parent_item_class(self):
        return _pitch.PitchClass

    @staticmethod
    def _get_most_compact_ordering(candidates):
        widths = []
        for candidate in candidates:
            if candidate[0] < candidate[-1]:
                width = abs(candidate[-1] - candidate[0])
            else:
                width = abs(candidate[-1] + 12 - candidate[0])
            widths.append(width)
        minimum_width = min(widths)
        candidates_ = []
        for candidate, width in zip(candidates, widths):
            if width == minimum_width:
                candidates_.append(candidate)
        candidates = candidates_
        assert 1 <= len(candidates)
        if len(candidates) == 1:
            segment = candidates[0]
            segment = PitchClassSegment(
                items=segment, item_class=_pitch.NumberedPitchClass
            )
            return segment
        for i in range(len(candidates[0]) - 1):
            widths = []
            for candidate in candidates:
                stop = i + 1
                if candidate[0] < candidate[stop]:
                    width = abs(candidate[stop] - candidate[0])
                else:
                    width = abs(candidate[stop] + 12 - candidate[0])
                widths.append(width)
            minimum_width = min(widths)
            candidates_ = []
            for candidate, width in zip(candidates, widths):
                if width == minimum_width:
                    candidates_.append(candidate)
            candidates = candidates_
            if len(candidates) == 1:
                segment = candidates[0]
                segment = PitchClassSegment(
                    items=segment, item_class=_pitch.NumberedPitchClass
                )
                return segment
        candidates.sort(key=lambda x: x[0])
        segment = candidates[0]
        segment = PitchClassSegment(items=segment, item_class=_pitch.NumberedPitchClass)
        return segment

    @classmethod
    def from_pitches(class_, pitches, item_class=None) -> "PitchClassSet":
        """
        Makes pitch-class set from ``pitches``.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> pitches = abjad.iterate.pitches([staff_1, staff_2])
            >>> abjad.PitchClassSet.from_pitches(pitches)
            PitchClassSet(items=['c', 'd', 'fs', 'g', 'a', 'b'], item_class=abjad.NamedPitchClass)

        """
        pitch_segment = PitchSegment.from_pitches(pitches)
        return class_(items=pitch_segment, item_class=item_class)

    def get_normal_order(self) -> "PitchClassSegment":
        """
        Gets normal order.

        ..  container:: example

            Gets normal order of empty pitch-class set:

            >>> pc_set = abjad.PitchClassSet()
            >>> pc_set.get_normal_order()
            PitchClassSegment(items=[], item_class=NumberedPitchClass)

        ..  container:: example

            Gets normal order:

            >>> pc_set = abjad.PitchClassSet([0, 1, 10, 11])
            >>> pc_set.get_normal_order()
            PitchClassSegment(items=[10, 11, 0, 1], item_class=NumberedPitchClass)

        ..  container:: example

            Gets normal order:

            >>> pc_set = abjad.PitchClassSet([2, 8, 9])
            >>> pc_set.get_normal_order()
            PitchClassSegment(items=[8, 9, 2], item_class=NumberedPitchClass)

        ..  container:: example

            Gets normal order of pitch-class set with degree of symmetry equal
            to 2:

            >>> pc_set = abjad.PitchClassSet([1, 2, 7, 8])
            >>> pc_set.get_normal_order()
            PitchClassSegment(items=[1, 2, 7, 8], item_class=NumberedPitchClass)

        ..  container:: example

            Gets normal order of pitch-class set with degree of symmetry equal
            to 4:

            >>> pc_set = abjad.PitchClassSet([0, 3, 6, 9])
            >>> pc_set.get_normal_order()
            PitchClassSegment(items=[0, 3, 6, 9], item_class=NumberedPitchClass)

        """
        if not len(self):
            return PitchClassSegment(items=None, item_class=_pitch.NumberedPitchClass)
        pitch_classes = list(self)
        pitch_classes.sort()
        candidates = []
        for i in range(self.cardinality):
            candidate_list = [_pitch.NumberedPitch(_) for _ in pitch_classes]
            candidate = _sequence.rotate(candidate_list, n=-i)
            candidates.append(candidate)
        return self._get_most_compact_ordering(candidates)

    def get_prime_form(self, transposition_only=False) -> "PitchClassSet":
        """
        Gets prime form.

        ..  container:: example

            Gets prime form of empty pitch-class set:

            >>> pc_set = abjad.PitchClassSet()
            >>> pc_set.get_prime_form()
            PitchClassSet(items=[], item_class=abjad.NamedPitchClass)

            >>> pc_set = abjad.PitchClassSet()
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet(items=[], item_class=abjad.NamedPitchClass)

        ..  container:: example

            Gets prime form:

            >>> pc_set = abjad.PitchClassSet([0, 1, 10, 11])
            >>> pc_set.get_prime_form()
            PitchClassSet(items=[0, 1, 2, 3], item_class=abjad.NumberedPitchClass)

            >>> pc_set = abjad.PitchClassSet([0, 1, 10, 11])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet(items=[0, 1, 2, 3], item_class=abjad.NumberedPitchClass)

        ..  container:: example

            Gets prime form:

            >>> pc_set = abjad.PitchClassSet([2, 8, 9])
            >>> pc_set.get_prime_form()
            PitchClassSet(items=[0, 1, 6], item_class=abjad.NumberedPitchClass)

            >>> pc_set = abjad.PitchClassSet([2, 8, 9])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet(items=[0, 1, 6], item_class=abjad.NumberedPitchClass)

        ..  container:: example

            Gets prime form of pitch-class set with degree of symmetry equal to
            2:

            >>> pc_set = abjad.PitchClassSet([1, 2, 7, 8])
            >>> pc_set.get_prime_form()
            PitchClassSet(items=[0, 1, 6, 7], item_class=abjad.NumberedPitchClass)

            >>> pc_set = abjad.PitchClassSet([1, 2, 7, 8])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet(items=[0, 1, 6, 7], item_class=abjad.NumberedPitchClass)

        ..  container:: example

            Gets prime form of pitch-class set with degree of symmetry equal to
            4:

            >>> pc_set = abjad.PitchClassSet([0, 3, 6, 9])
            >>> pc_set.get_prime_form()
            PitchClassSet(items=[0, 3, 6, 9], item_class=abjad.NumberedPitchClass)

            >>> pc_set = abjad.PitchClassSet([0, 3, 6, 9])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet(items=[0, 3, 6, 9], item_class=abjad.NumberedPitchClass)

        ..  container:: example

            Gets prime form of pitch-class that is not inversion-equivalent:

            >>> pc_set = abjad.PitchClassSet([0, 4, 6, 7])
            >>> pc_set.get_prime_form()
            PitchClassSet(items=[0, 1, 3, 7], item_class=abjad.NumberedPitchClass)

            >>> pc_set = abjad.PitchClassSet([0, 4, 6, 7])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet(items=[0, 4, 6, 7], item_class=abjad.NumberedPitchClass)

        ..  container:: example

            Gets prime form of inversionally nonequivalent pitch-class set:

            >>> pc_set = abjad.PitchClassSet([0, 4, 7])
            >>> pc_set.get_prime_form()
            PitchClassSet(items=[0, 3, 7], item_class=abjad.NumberedPitchClass)

            >>> pc_set = abjad.PitchClassSet([0, 4, 7])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet(items=[0, 4, 7], item_class=abjad.NumberedPitchClass)

        ..  container:: example

            REGRESSION:

            >>> pc_set = abjad.PitchClassSet([0, 1, 2, 5, 8, 9])
            >>> pc_set.get_prime_form()
            PitchClassSet(items=[0, 1, 2, 5, 6, 9], item_class=abjad.NumberedPitchClass)

            REGRESSION:

            >>> pc_set = abjad.PitchClassSet([0, 1, 2, 3, 6, 7])
            >>> pc_set.get_prime_form()
            PitchClassSet(items=[0, 1, 2, 3, 6, 7], item_class=abjad.NumberedPitchClass)

        Returns new pitch-class set.
        """
        if not len(self):
            return copy.copy(self)
        normal_order = self.get_normal_order()
        if not transposition_only:
            normal_orders = [normal_order]
            inversion = self.invert()
            normal_order = inversion.get_normal_order()
            normal_orders.append(normal_order)
            normal_orders = [_._transpose_to_zero() for _ in normal_orders]
            assert len(normal_orders) == 2
            for left_pc, right_pc in zip(*normal_orders):
                if left_pc == right_pc:
                    continue
                if left_pc < right_pc:
                    normal_order = normal_orders[0]
                    break
                if right_pc < left_pc:
                    normal_order = normal_orders[-1]
                    break
        pcs = [_.number for _ in normal_order]
        first_pc = pcs[0]
        pcs = [pc - first_pc for pc in pcs]
        prime_form = type(self)(items=pcs, item_class=_pitch.NumberedPitchClass)
        return prime_form

    def invert(self, axis=None) -> "PitchClassSet":
        """
        Inverts pitch-class set.

        ..  container:: example

            >>> abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ... ).invert()
            PitchClassSet(items=[1.5, 2, 5, 6], item_class=abjad.NumberedPitchClass)

        """
        return type(self)([pc.invert(axis=axis) for pc in self.items])

    def is_transposed_subset(self, pcset) -> bool:
        """
        Is true when pitch-class set is transposed subset of ``pcset``.

        ..  container:: example

            >>> pitch_class_set_1 = abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ... )
            >>> pitch_class_set_2 = abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7, 7.5, 8],
            ... )

            >>> pitch_class_set_1.is_transposed_subset(pitch_class_set_2)
            True

        """
        for n in range(12):
            if self.transpose(n).issubset(pcset):
                return True
        return False

    def is_transposed_superset(self, pcset) -> bool:
        """
        Is true when pitch-class set is transposed superset of ``pcset``.

        ..  container:: example

            >>> pitch_class_set_1 = abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ... )
            >>> pitch_class_set_2 = abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7, 7.5, 8],
            ... )

            >>> pitch_class_set_2.is_transposed_superset(pitch_class_set_1)
            True

        """
        for n in range(12):
            if self.transpose(n).issuperset(pcset):
                return True
        return False

    def multiply(self, n) -> "PitchClassSet":
        """
        Multiplies pitch-class set by ``n``.

        ..  container:: example

            >>> abjad.PitchClassSet(
            ...     [-2, -1.5, 6, 7, -1.5, 7],
            ... ).multiply(5)
            PitchClassSet(items=[2, 4.5, 6, 11], item_class=abjad.NumberedPitchClass)

        """
        items = (pitch_class.multiply(n) for pitch_class in self)
        return dataclasses.replace(self, items=items)

    def order_by(self, segment) -> "PitchClassSegment":
        """
        Orders pitch-class set by pitch-class ``segment``.

        ..  container:: example

            >>> set_ = abjad.PitchClassSet(["c", "e", "b"])
            >>> segment = abjad.PitchClassSegment(["e", "a", "f"])
            >>> set_.order_by(segment)
            PitchClassSegment(items="b e c", item_class=NamedPitchClass)

        """
        if not len(self) == len(segment):
            raise ValueError("set and segment must be on equal length.")
        for pitch_classes in _enumerate.yield_permutations(list(self)):
            candidate = PitchClassSegment(pitch_classes)
            if candidate._is_equivalent_under_transposition(segment):
                return candidate
        raise ValueError(f"{self!s} can not order by {segment!s}.")

    def transpose(self, n=0) -> "PitchClassSet":
        """
        Transposes all pitch-classes in pitch-class set by index ``n``.

        ..  container:: example

            >>> set_ = abjad.PitchClassSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitchClass,
            ... )

            >>> for n in range(12):
            ...     print(n, set_.transpose(n))
            ...
            0 PC{6, 7, 10, 10.5}
            1 PC{7, 8, 11, 11.5}
            2 PC{0, 0.5, 8, 9}
            3 PC{1, 1.5, 9, 10}
            4 PC{2, 2.5, 10, 11}
            5 PC{0, 3, 3.5, 11}
            6 PC{0, 1, 4, 4.5}
            7 PC{1, 2, 5, 5.5}
            8 PC{2, 3, 6, 6.5}
            9 PC{3, 4, 7, 7.5}
            10 PC{4, 5, 8, 8.5}
            11 PC{5, 6, 9, 9.5}

        """
        items = (pitch_class + n for pitch_class in self)
        return dataclasses.replace(self, items=items)


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class PitchSet(Set):
    r"""
    Pitch set.

    ..  container:: example

        Numbered pitch set:

        >>> set_ = abjad.PitchSet(
        ...     items=[-2, -1.5, 6, 7, -1.5, 7],
        ...     item_class=abjad.NumberedPitch,
        ... )
        >>> set_
        PitchSet(items=[-2, -1.5, 6, 7], item_class=abjad.NumberedPitch)

    ..  container:: example

        Named pitch set:

        >>> set_ = abjad.PitchSet(
        ...     ["bf,", "aqs", "fs'", "g'", "bqf", "g'"],
        ...     item_class=abjad.NamedPitch,
        ... )
        >>> set_
        PitchSet(items=['bf,', 'aqs', 'bqf', "fs'", "g'"], item_class=abjad.NamedPitch)

    ..  container:: example

        >>> set_1 = abjad.PitchSet(
        ...     items=[-2, -1.5, 6, 7, -1.5, 7],
        ...     item_class=abjad.NumberedPitch,
        ... )
        >>> set_2 = abjad.PitchSet(
        ...     items=[-2, -1.5, 6, 7, -1.5, 7],
        ...     item_class=abjad.NumberedPitch,
        ... )
        >>> set_3 = abjad.PitchSet(
        ...     items=[11, 12, 12.5],
        ...     item_class=abjad.NumberedPitch,
        ... )

        >>> set_1 == set_1
        True
        >>> set_1 == set_2
        True
        >>> set_1 == set_3
        False

        >>> set_2 == set_1
        True
        >>> set_2 == set_2
        True
        >>> set_2 == set_3
        False

        >>> set_3 == set_1
        False
        >>> set_3 == set_2
        False
        >>> set_3 == set_3
        True

    """

    def __repr__(self):
        """
        Gets repr of pitch-class set.
        """
        return f"{type(self).__name__}(items={self._get_sorted_repr_items()}, item_class=abjad.{self.item_class.__name__})"

    @property
    def _named_item_class(self):
        return _pitch.NamedPitch

    @property
    def _numbered_item_class(self):
        return _pitch.NumberedPitch

    @property
    def _parent_item_class(self):
        return _pitch.Pitch

    def _is_equivalent_under_transposition(self, argument):
        """
        True if pitch set is equivalent to ``argument`` under transposition.

        Returns true or false.
        """
        if not isinstance(argument, type(self)):
            return False
        if not len(self) == len(argument):
            return False
        difference = -(
            _pitch.NamedPitch(argument[0], 4) - _pitch.NamedPitch(self[0], 4)
        )
        new_pitches = (x + difference for x in self)
        new_pitches = dataclasses.replace(self, items=new_pitches)
        return argument == new_pitches

    def _sort_self(self):
        return sorted(PitchSegment(tuple(self)))

    @property
    def duplicate_pitch_classes(self) -> "PitchClassSet":
        """
        Gets duplicate pitch-classes in pitch set.

        ..  container:: example

            >>> set_ = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ... )
            >>> set_.duplicate_pitch_classes
            PitchClassSet(items=[], item_class=abjad.NumberedPitchClass)

            >>> set_ = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, 10.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ... )
            >>> set_.duplicate_pitch_classes
            PitchClassSet(items=[10.5], item_class=abjad.NumberedPitchClass)

        """
        pitch_classes = []
        duplicate_pitch_classes = []
        for pitch in self:
            pitch_class = _pitch.NumberedPitchClass(pitch)
            if pitch_class in pitch_classes:
                duplicate_pitch_classes.append(pitch_class)
            pitch_classes.append(pitch_class)
        return PitchClassSet(
            duplicate_pitch_classes, item_class=_pitch.NumberedPitchClass
        )

    @property
    def hertz(self) -> set[float]:
        """
        Gets hertz of pitches in pitch segment.

        ..  container:: example

            >>> pitch_set = abjad.PitchSet("c e g b")
            >>> sorted(pitch_set.hertz)
            [130.81..., 164.81..., 195.99..., 246.94...]

        """
        return set(_.hertz for _ in self)

    @property
    def is_pitch_class_unique(self) -> bool:
        """
        Is true when pitch set is pitch-class-unique.

        ..  container:: example

            >>> set_ = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ... )

            >>> set_.is_pitch_class_unique
            True

        ..  container:: example

            >>> set_ = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, 10.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ... )

            >>> set_.is_pitch_class_unique
            False

        """
        numbered_pitch_class_set = PitchClassSet(
            self, item_class=_pitch.NumberedPitchClass
        )
        return len(self) == len(numbered_pitch_class_set)

    @classmethod
    def from_pitches(class_, pitches, item_class=None) -> "PitchSet":
        """
        Makes pitch set from ``pitches``.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> pitches = abjad.iterate.pitches([staff_1, staff_2])
            >>> abjad.PitchSet.from_pitches(pitches)
            PitchSet(items=['c', 'g', 'b', "c'", "d'", "fs'", "a'"], item_class=abjad.NamedPitch)

        """
        pitch_segment = PitchSegment.from_pitches(pitches)
        return class_(items=pitch_segment, item_class=item_class)

    def invert(self, axis) -> "PitchSet":
        """
        Inverts pitch set about ``axis``.
        """
        items = (pitch.invert(axis) for pitch in self)
        return dataclasses.replace(self, items=items)

    def issubset(self, argument) -> bool:
        """
        Is true when pitch set is subset of ``argument``.

        ..  container:: example

            >>> set_1 = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ... )
            >>> set_2 = abjad.PitchSet(
            ...     items=[-1.5, 6],
            ...     item_class=abjad.NumberedPitch,
            ... )

            >>> set_1.issubset(set_2)
            False

            >>> set_2.issubset(set_1)
            True

        """
        return Set.issubset(self, argument)

    def issuperset(self, argument) -> bool:
        """
        Is true when pitch set is superset of ``argument``.

        ..  container:: example

            >>> set_1 = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ... )
            >>> set_2 = abjad.PitchSet(
            ...     items=[-1.5, 6],
            ...     item_class=abjad.NumberedPitch,
            ... )

            >>> set_1.issuperset(set_2)
            False

            >>> set_2.issuperset(set_1)
            True

        """
        return Set.issubset(self, argument)

    def register(self, pitch_classes):
        """
        Registers ``pitch_classes`` by pitch set.

        ..  container:: example

            >>> pitch_set = abjad.PitchSet(
            ...     items=[10, 19, 20, 23, 24, 26, 27, 29, 30, 33, 37, 40],
            ...     item_class=abjad.NumberedPitch,
            ... )
            >>> pitch_classes = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
            >>> pitches = pitch_set.register(pitch_classes)
            >>> for pitch in pitches:
            ...     pitch
            NumberedPitch(10)
            NumberedPitch(24)
            NumberedPitch(26)
            NumberedPitch(30)
            NumberedPitch(20)
            NumberedPitch(19)
            NumberedPitch(29)
            NumberedPitch(27)
            NumberedPitch(37)
            NumberedPitch(33)
            NumberedPitch(40)
            NumberedPitch(23)

        Returns list of zero or more numbered pitches.
        """
        if isinstance(pitch_classes, collections.abc.Iterable):
            result = [
                [_ for _ in self if _.number % 12 == pc]
                for pc in [x % 12 for x in pitch_classes]
            ]
            result = _sequence.flatten(result, depth=-1)
        elif isinstance(pitch_classes, int):
            result = [p for p in pitch_classes if p % 12 == pitch_classes][0]
        else:
            raise TypeError("must be pitch-class or list of pitch-classes.")
        return result

    def transpose(self, n=0) -> "PitchSet":
        """
        Transposes pitch set by index ``n``.
        """
        items = (pitch.transpose(n=n) for pitch in self)
        return dataclasses.replace(self, items=items)


def make_interval_class_vector(pitches):
    """
    Makes interval-class vector.
    """
    intervals = []
    pairs = _enumerate.yield_pairs(list(pitches))
    for first, second in pairs:
        intervals.append(second - first)
    items = [_pitch.NumberedInversionEquivalentIntervalClass(_) for _ in intervals]
    counter = collections.Counter(items)
    counts = []
    for i in range(7):
        item = _pitch.NumberedInversionEquivalentIntervalClass(i)
        count = counter.get(item, 0)
        counts.append(count)
    counts = "".join([str(_) for _ in counts])
    if len(counter) == 13:
        quartertones = []
        for i in range(6):
            item = _pitch.NumberedInversionEquivalentIntervalClass(i + 0.5)
            count = counter.get(item, 0)
            quartertones.append(count)
        quartertones = "".join([str(_) for _ in quartertones])
        string = rf'\tiny \column {{ "{counts}" "{quartertones}" }}'
    else:
        string = rf"\tiny {counts}"
    return string
