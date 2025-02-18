import collections
import copy
import dataclasses
import functools
import types
import typing

from . import enumerate as _enumerate
from . import pitch as _pitch
from . import sequence as _sequence


@dataclasses.dataclass(slots=True)
class PitchClassSegment:
    r"""
    Numbered pitch-class segment.

    ..  container:: example

        >>> segment = abjad.PitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])
        >>> segment
        PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

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

    """

    items: typing.Sequence = ()

    def __post_init__(self):
        self.items = tuple(_pitch.NumberedPitchClass(_) for _ in self.items or [])

    def __add__(self, argument) -> "PitchClassSegment":
        """
        Adds ``argument`` to numbered pitch-class segment.
        """
        assert isinstance(argument, type(self)), repr(argument)
        items = tuple(self.items) + tuple(argument.items)
        return type(self)(items)

    def __contains__(self, argument) -> bool:
        """
        Is true when numbered pitch-class segment contains ``argument``.
        """
        return argument in self.items

    def __getitem__(self, argument):
        """
        Gets ``argument`` from numbered pitch-class segment.
        """
        item = self.items.__getitem__(argument)
        if isinstance(item, tuple):
            return type(self)(item)
        else:
            return item

    def __iter__(self):
        """
        Iterates numbered pitch-class segment.
        """
        return self.items.__iter__()

    def __len__(self):
        """
        Gets length of numbered pitch-class segment.
        """
        return len(self.items)

    def __mul__(self, n) -> "PitchClassSegment":
        r"""
        Multiplies numbered pitch-class segment by ``n``.

        ..  container:: example

            >>> segment = abjad.PitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> 2 * segment
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7])

        """
        return type(self)(n * self.items)

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        items = [_.number for _ in self.items]
        return f"{type(self).__name__}({items!r})"

    def __rmul__(self, n) -> "PitchClassSegment":
        r"""
        Multiplies ``n`` by numbered pitch-class segment.

        ..  container:: example

            >>> segment = abjad.PitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> segment * 2
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7, 10, 10.5, 6, 7, 10.5, 7])

        """
        return type(self)(self.items * n)

    def __str__(self) -> str:
        r"""
        Gets string representation of numbered pitch-class segment.

        ..  container::

            >>> segment = abjad.PitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])
            >>> str(segment)
            'PC<10, 10.5, 6, 7, 10.5, 7>'

        """
        string = ", ".join([str(_.number) for _ in self])
        return f"PC<{string}>"

    def invert(self, axis=None) -> "PitchClassSegment":
        r"""
        Inverts numbered pitch-class segment.

        ..  container:: example

            >>> segment = abjad.PitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> segment.invert()
            PitchClassSegment([2, 1.5, 6, 5, 1.5, 5])

            >>> segment.invert().invert()
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

        """
        items = [_.invert(axis=axis) for _ in self]
        return type(self)(items)

    def multiply(self, n=1) -> "PitchClassSegment":
        r"""
        Multiplies pitch-classes in numbered pitch-class segment by ``n``.

        ..  container:: example

            >>> segment = abjad.PitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])
            >>> segment
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> segment.multiply(n=1)
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> segment.multiply(n=5)
            PitchClassSegment([2, 4.5, 6, 11, 4.5, 11])

            >>> segment.multiply(n=7)
            PitchClassSegment([10, 1.5, 6, 1, 1.5, 1])

            >>> segment.multiply(n=99)
            PitchClassSegment([6, 7.5, 6, 9, 7.5, 9])

        """
        items = [_.multiply(n=n) for _ in self]
        return type(self)(items)

    def retrograde(self) -> "PitchClassSegment":
        r"""
        Gets retrograde of numbered pitch-class segment.

        ..  container:: example

            >>> segment = abjad.PitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> segment.retrograde()
            PitchClassSegment([7, 10.5, 7, 6, 10.5, 10])

            >>> segment.retrograde().retrograde()
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

        """
        items = tuple(reversed(self.items))
        return type(self)(items)

    def rotate(self, n=0) -> "PitchClassSegment":
        r"""
        Rotates numbered pitch-class segment by index ``n``.

        ..  container:: example

            >>> segment = abjad.PitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> segment.rotate(n=1)
            PitchClassSegment([7, 10, 10.5, 6, 7, 10.5])

            >>> segment.rotate(n=-1)
            PitchClassSegment([10.5, 6, 7, 10.5, 7, 10])

            >>> segment.rotate(n=0)
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

        """
        items = _sequence.rotate(self.items, n=n)
        return type(self)(items)

    def transpose(self, n=0) -> "PitchClassSegment":
        r"""
        Transposes numbered pitch-class segment by index ``n``.

        ..  container:: example

            >>> segment = abjad.PitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> segment.transpose(n=11)
            PitchClassSegment([9, 9.5, 5, 6, 9.5, 6])

        """
        items = [_.transpose(n=n) for _ in self]
        return type(self)(items)


collections.abc.Sequence.register(PitchClassSegment)


class PitchClassSet(frozenset):
    """
    Numbered pitch-class set.

    ..  container:: example

        >>> set_ = abjad.PitchClassSet([-2, -1.5, 6, 7, -1.5, 7])
        >>> set_
        PitchClassSet([6, 7, 10, 10.5])

        >>> str(set_)
        'PC{6, 7, 10, 10.5}'

        >>> abjad.NamedPitch("fs") in set_
        False

        >>> abjad.NamedPitch("f") in set_
        False

        >>> 6 in set_
        False

        >>> 5 in set_
        False

        >>> abjad.NumberedPitchClass(5) in set_
        False

        >>> abjad.NumberedPitchClass(6) in set_
        True

    ..  container:: example

        Classical operators:

        >>> set_1 = abjad.PitchClassSet([0, 2, 4, 5])
        >>> set_2 = abjad.PitchClassSet([4, 5, 9])

        >>> set_1 & set_2
        PitchClassSet([4, 5])

        >>> set_1 | set_2
        PitchClassSet([0, 2, 4, 5, 9])

        >>> set_1 ^ set_2
        PitchClassSet([0, 2, 9])

        >>> set_1 - set_2
        PitchClassSet([0, 2])

        >>> set_2 - set_1
        PitchClassSet([9])

    """

    def __new__(class_, argument=()):
        if isinstance(argument, str):
            argument = argument.split()
        argument = [_pitch.NumberedPitchClass(_) for _ in argument]
        self = frozenset.__new__(class_, argument)
        return self

    @classmethod
    def _wrap_methods(class_, names):
        def closure(name):
            def inner(self, *arguments):
                result = getattr(super(class_, self), name)(*arguments)
                result = PitchClassSet(result)
                return result

            inner.fn_name = name
            setattr(class_, name, inner)

        for name in names:
            closure(name)

    def __repr__(self):
        numbers = [_.number for _ in self]
        numbers.sort()
        return f"{type(self).__name__}({numbers!r})"

    def __str__(self) -> str:
        numbers = [_.number for _ in self]
        numbers.sort()
        string = ", ".join(str(_) for _ in numbers)
        return f"PC{{{string}}}"

    @property
    def cardinality(self):
        return len(self)

    def get_normal_order(self) -> "PitchClassSegment":
        """
        Gets normal order.

        ..  container:: example

            Gets normal order of empty pitch-class set:

            >>> pc_set = abjad.PitchClassSet()
            >>> pc_set.get_normal_order()
            PitchClassSegment([])

        ..  container:: example

            Gets normal order:

            >>> pc_set = abjad.PitchClassSet([0, 1, 10, 11])
            >>> pc_set.get_normal_order()
            PitchClassSegment([10, 11, 0, 1])

        ..  container:: example

            Gets normal order:

            >>> pc_set = abjad.PitchClassSet([2, 8, 9])
            >>> pc_set.get_normal_order()
            PitchClassSegment([8, 9, 2])

        ..  container:: example

            Gets normal order of pitch-class set with degree of symmetry equal
            to 2:

            >>> pc_set = abjad.PitchClassSet([1, 2, 7, 8])
            >>> pc_set.get_normal_order()
            PitchClassSegment([1, 2, 7, 8])

        ..  container:: example

            Gets normal order of pitch-class set with degree of symmetry equal
            to 4:

            >>> pc_set = abjad.PitchClassSet([0, 3, 6, 9])
            >>> pc_set.get_normal_order()
            PitchClassSegment([0, 3, 6, 9])

        """
        if not len(self):
            return PitchClassSegment()
        pitch_classes = list(self)
        pitch_classes.sort()
        candidates = []
        for i in range(self.cardinality):
            candidate_list = [_pitch.NumberedPitch(_) for _ in pitch_classes]
            candidate = _sequence.rotate(candidate_list, n=-i)
            candidates.append(candidate)
        return _get_most_compact_ordering(candidates)

    def get_prime_form(self, transposition_only=False) -> "PitchClassSet":
        """
        Gets prime form.

        ..  container:: example

            Gets prime form of empty pitch-class set:

            >>> pc_set = abjad.PitchClassSet()
            >>> pc_set.get_prime_form()
            PitchClassSet([])

            >>> pc_set = abjad.PitchClassSet()
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([])

        ..  container:: example

            Gets prime form:

            >>> pc_set = abjad.PitchClassSet([0, 1, 10, 11])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 1, 2, 3])

            >>> pc_set = abjad.PitchClassSet([0, 1, 10, 11])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([0, 1, 2, 3])

        ..  container:: example

            Gets prime form:

            >>> pc_set = abjad.PitchClassSet([2, 8, 9])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 1, 6])

            >>> pc_set = abjad.PitchClassSet([2, 8, 9])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([0, 1, 6])

        ..  container:: example

            Gets prime form of pitch-class set with degree of symmetry equal to
            2:

            >>> pc_set = abjad.PitchClassSet([1, 2, 7, 8])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 1, 6, 7])

            >>> pc_set = abjad.PitchClassSet([1, 2, 7, 8])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([0, 1, 6, 7])

        ..  container:: example

            Gets prime form of pitch-class set with degree of symmetry equal to
            4:

            >>> pc_set = abjad.PitchClassSet([0, 3, 6, 9])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 3, 6, 9])

            >>> pc_set = abjad.PitchClassSet([0, 3, 6, 9])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([0, 3, 6, 9])

        ..  container:: example

            Gets prime form of pitch-class that is not inversion-equivalent:

            >>> pc_set = abjad.PitchClassSet([0, 4, 6, 7])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 1, 3, 7])

            >>> pc_set = abjad.PitchClassSet([0, 4, 6, 7])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([0, 4, 6, 7])

        ..  container:: example

            Gets prime form of inversionally nonequivalent pitch-class set:

            >>> pc_set = abjad.PitchClassSet([0, 4, 7])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 3, 7])

            >>> pc_set = abjad.PitchClassSet([0, 4, 7])
            >>> pc_set.get_prime_form(transposition_only=True)
            PitchClassSet([0, 4, 7])

        ..  container:: example

            REGRESSION:

            >>> pc_set = abjad.PitchClassSet([0, 1, 2, 5, 8, 9])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 1, 2, 5, 6, 9])

            REGRESSION:

            >>> pc_set = abjad.PitchClassSet([0, 1, 2, 3, 6, 7])
            >>> pc_set.get_prime_form()
            PitchClassSet([0, 1, 2, 3, 6, 7])

        Returns new pitch-class set.
        """

        def _transpose_to_zero(segment):
            numbers = [_.number for _ in segment]
            first_number = segment[0].number
            numbers = [pc.number - first_number for pc in segment]
            pcs = [_ % 12 for _ in numbers]
            return type(segment)(pcs)

        if not len(self):
            return copy.copy(self)
        normal_order = self.get_normal_order()
        if not transposition_only:
            normal_orders = [normal_order]
            inversion = self.invert()
            normal_order = inversion.get_normal_order()
            normal_orders.append(normal_order)
            normal_orders = [_transpose_to_zero(_) for _ in normal_orders]
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
        prime_form = type(self)(pcs)
        return prime_form

    def invert(self, axis=None) -> "PitchClassSet":
        """
        Inverts pitch-class set.

        ..  container:: example

            >>> abjad.PitchClassSet([-2, -1.5, 6, 7, -1.5, 7]).invert()
            PitchClassSet([1.5, 2, 5, 6])

        """
        return type(self)([_.invert(axis=axis) for _ in self])

    def multiply(self, n) -> "PitchClassSet":
        """
        Multiplies pitch-class set by ``n``.

        ..  container:: example

            >>> abjad.PitchClassSet([-2, -1.5, 6, 7, -1.5, 7]).multiply(5)
            PitchClassSet([2, 4.5, 6, 11])

        """
        return type(self)(_.multiply(n) for _ in self)

    def transpose(self, n=0) -> "PitchClassSet":
        """
        Transposes all pitch-classes in pitch-class set by index ``n``.

        ..  container:: example

            >>> set_ = abjad.PitchClassSet([-2, -1.5, 6, 7, -1.5, 7])
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
        return type(self)(_ + n for _ in self)


collections.abc.Sequence.register(PitchClassSet)


PitchClassSet._wrap_methods(
    [
        "__and__",
        "__or__",
        "__sub__",
        "__xor__",
        "difference",
        "intersection",
        "symmetric_difference",
        "union",
    ]
)


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
                        \context Voice = "Treble_Voice"
                        {
                            \clef "treble"
                            s1 * 1/4
                            s1 * 1/4
                        }
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \context Voice = "Bass_Voice"
                        {
                            \clef "bass"
                            c1 * 1/4
                            \glissando
                            \change Staff = Treble_Staff
                            c''''1 * 1/4
                        }
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
        namespace = self._parse_range_string(range_string)
        assert isinstance(namespace.start_pitch, _pitch.NamedPitch | type(None))
        assert isinstance(namespace.stop_pitch, _pitch.NamedPitch | type(None))
        self._close_bracket = namespace.close_bracket
        self._open_bracket = namespace.open_bracket
        self._range_string = namespace.range_string
        self._start_pitch = namespace.start_pitch
        self._stop_pitch = namespace.stop_pitch

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
        if isinstance(argument, str | _pitch.NamedPitch):
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
class PitchSegment:
    r"""
    Named pitch segment.

    ..  container:: example

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
                    \context Voice = "Treble_Voice"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                }
            >>

    """

    items: typing.Sequence = ()

    def __post_init__(self):
        self.items = tuple(_pitch.NumberedPitch(_) for _ in self.items or [])

    def __contains__(self, argument) -> bool:
        """
        Is true when named pitch segment contains ``argument``.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> abjad.NamedPitch("fs'") in segment
            False

            >>> abjad.NamedPitch(6) in segment
            False

            >>> abjad.NamedPitch("fs") in segment
            False

            >>> 6 in segment
            True

            >>> abjad.NumberedPitch(6) in segment
            True

            >>> abjad.NumberedPitch("fs'") in segment
            True

            >>> abjad.NamedPitch("f") in segment
            False

            >>> 5 in segment
            False

        """
        return argument in self.items

    def __getitem__(self, argument):
        """
        Gets item at ``argument`` in named pitch segment.
        """
        return self.items.__getitem__(argument)

    def __iter__(self):
        """
        Iterates named pitch segment.
        """
        return self.items.__iter__()

    def __len__(self):
        """
        Gets length of named pitch segment.
        """
        return len(self.items)

    def __repr__(self):
        """
        Gets repr.
        """
        numbers = [_.number for _ in self.items]
        return f"{type(self).__name__}({numbers})"

    def __str__(self) -> str:
        """
        Gets string.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> str(segment)
            '<-2, -1.5, 6, 7, -1.5, 7>'

        """
        string = ", ".join([str(_.number) for _ in self])
        return f"<{string}>"

    def invert(self, axis=None) -> "PitchSegment":
        r"""
        Inverts named pitch segment about ``axis``.

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
                        \context Voice = "Treble_Voice"
                        {
                            \clef "treble"
                            r1 * 1/8
                            r1 * 1/8
                            fs'1 * 1/8
                            g'1 * 1/8
                            r1 * 1/8
                            g'1 * 1/8
                        }
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \context Voice = "Bass_Voice"
                        {
                            \clef "bass"
                            bf1 * 1/8
                            bqf1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            bqf1 * 1/8
                            r1 * 1/8
                        }
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
                        \context Voice = "Treble_Voice"
                        {
                            \clef "treble"
                            d'1 * 1/8
                            dqf'1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            dqf'1 * 1/8
                            r1 * 1/8
                        }
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \context Voice = "Bass_Voice"
                        {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            fs1 * 1/8
                            f1 * 1/8
                            r1 * 1/8
                            f1 * 1/8
                        }
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
                        \context Voice = "Treble_Voice"
                        {
                            \clef "treble"
                            r1 * 1/8
                            r1 * 1/8
                            fs'1 * 1/8
                            g'1 * 1/8
                            r1 * 1/8
                            g'1 * 1/8
                        }
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \context Voice = "Bass_Voice"
                        {
                            \clef "bass"
                            bf1 * 1/8
                            bqf1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            bqf1 * 1/8
                            r1 * 1/8
                        }
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
                        \context Voice = "Treble_Voice"
                        {
                            \clef "treble"
                            r1 * 1/8
                            r1 * 1/8
                            fs''1 * 1/8
                            a''1 * 1/8
                            r1 * 1/8
                            a''1 * 1/8
                        }
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \context Voice = "Bass_Voice"
                        {
                            \clef "bass"
                            fs1 * 1/8
                            gqs1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            gqs1 * 1/8
                            r1 * 1/8
                        }
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
                        \context Voice = "Treble_Voice"
                        {
                            \clef "treble"
                            r1 * 1/8
                            r1 * 1/8
                            fs'1 * 1/8
                            g'1 * 1/8
                            r1 * 1/8
                            g'1 * 1/8
                        }
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \context Voice = "Bass_Voice"
                        {
                            \clef "bass"
                            bf1 * 1/8
                            bqf1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            bqf1 * 1/8
                            r1 * 1/8
                        }
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
                        \context Voice = "Treble_Voice"
                        {
                            \clef "treble"
                            g'1 * 1/8
                            r1 * 1/8
                            g'1 * 1/8
                            fs'1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                        }
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \context Voice = "Bass_Voice"
                        {
                            \clef "bass"
                            r1 * 1/8
                            bqf1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            bqf1 * 1/8
                            bf1 * 1/8
                        }
                    }
                >>

        """
        return dataclasses.replace(self, items=list(reversed(self)))

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
                        \context Voice = "Treble_Voice"
                        {
                            \clef "treble"
                            r1 * 1/8
                            r1 * 1/8
                            fs'1 * 1/8
                            g'1 * 1/8
                            r1 * 1/8
                            g'1 * 1/8
                        }
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \context Voice = "Bass_Voice"
                        {
                            \clef "bass"
                            bf1 * 1/8
                            bqf1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            bqf1 * 1/8
                            r1 * 1/8
                        }
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
                        \context Voice = "Treble_Voice"
                        {
                            \clef "treble"
                            g'1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            fs'1 * 1/8
                            g'1 * 1/8
                            r1 * 1/8
                        }
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \context Voice = "Bass_Voice"
                        {
                            \clef "bass"
                            r1 * 1/8
                            bf1 * 1/8
                            bqf1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            bqf1 * 1/8
                        }
                    }
                >>

        """
        rotated_pitches = _sequence.rotate(self.items, n=n)
        new_segment = dataclasses.replace(self, items=rotated_pitches)
        return new_segment

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
                        \context Voice = "Treble_Voice"
                        {
                            \clef "treble"
                            r1 * 1/8
                            r1 * 1/8
                            fs'1 * 1/8
                            g'1 * 1/8
                            r1 * 1/8
                            g'1 * 1/8
                        }
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \context Voice = "Bass_Voice"
                        {
                            \clef "bass"
                            bf1 * 1/8
                            bqf1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            bqf1 * 1/8
                            r1 * 1/8
                        }
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
                        \context Voice = "Treble_Voice"
                        {
                            \clef "treble"
                            a'1 * 1/8
                            aqs'1 * 1/8
                            f''1 * 1/8
                            fs''1 * 1/8
                            aqs'1 * 1/8
                            fs''1 * 1/8
                        }
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \context Voice = "Bass_Voice"
                        {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                        }
                    }
                >>

        """
        if isinstance(n, int | float):
            interval = _pitch.NumberedInterval(n)
        else:
            interval = n
        assert isinstance(interval, _pitch.NumberedInterval), repr(interval)
        items = [_.transpose(n=interval) for _ in self]
        return type(self)(items)


collections.abc.Sequence.register(PitchSegment)


class PitchSet(frozenset):
    """
    Numbered pitch set.

    ..  container:: example

        >>> set_1 = abjad.PitchSet([-26, -2.5, 6, 7, -1.5, 7])
        >>> set_2 = abjad.PitchSet([-1.5, 7, 9, 12])

        >>> set_1
        PitchSet([-26, -2.5, -1.5, 6, 7])

        >>> set_2
        PitchSet([-1.5, 7, 9, 12])

        >>> str(set_1)
        '{-26, -2.5, -1.5, 6, 7}'

        >>> str(set_2)
        '{-1.5, 7, 9, 12}'

        >>> -1.5 in set_1
        False

        >>> abjad.NumberedPitch(-1.5) in set_1
        True

        >>> abjad.NumberedPitch("aqs") in set_2
        False

        >>> len(set_1)
        5

        >>> len(set_2)
        4

    ..  container:: example

        Classical operators:

        >>> set_1 = abjad.PitchSet([-26, -2.5, 6, 7, -1.5, 7])
        >>> set_2 = abjad.PitchSet([-1.5, 7, 9, 12])

        >>> set_1 & set_2
        PitchSet([-1.5, 7])

        >>> set_2 & set_1
        PitchSet([-1.5, 7])

        >>> set_1.intersection(set_2)
        PitchSet([-1.5, 7])

        >>> set_2.intersection(set_1)
        PitchSet([-1.5, 7])

        >>> set_1 | set_2
        PitchSet([-26, -2.5, -1.5, 6, 7, 9, 12])

        >>> set_2 | set_1
        PitchSet([-26, -2.5, -1.5, 6, 7, 9, 12])

        >>> set_1.union(set_2)
        PitchSet([-26, -2.5, -1.5, 6, 7, 9, 12])

        >>> set_2.union(set_1)
        PitchSet([-26, -2.5, -1.5, 6, 7, 9, 12])

        >>> set_1 - set_2
        PitchSet([-26, -2.5, 6])

        >>> set_1.difference(set_2)
        PitchSet([-26, -2.5, 6])

        >>> set_2 - set_1
        PitchSet([9, 12])

        >>> set_2.difference(set_1)
        PitchSet([9, 12])

        >>> set_1 ^ set_2
        PitchSet([-26, -2.5, 6, 9, 12])

        >>> set_2 ^ set_1
        PitchSet([-26, -2.5, 6, 9, 12])

        >>> set_1.symmetric_difference(set_2)
        PitchSet([-26, -2.5, 6, 9, 12])

        >>> set_2.symmetric_difference(set_1)
        PitchSet([-26, -2.5, 6, 9, 12])

    ..  container:: example

        >>> set_1 = abjad.PitchSet([-6, -5, -3, -1])
        >>> set_2 = abjad.PitchSet([-3, -1])
        >>> set_3 = abjad.PitchSet([1, 3, 4])

        Predicates:

        >>> set_1.isdisjoint(set_3)
        True

        >>> set_2.issubset(set_1)
        True

        >>> set_1.issuperset(set_2)
        True

    ..  container:: example

        >>> set_1 = abjad.PitchSet([-26, -2.5, 6, 7, -1.5, 7])
        >>> set_2 = abjad.PitchSet([-1.5, 7, 9, 12])

        Comparison:

        >>> set_1 == set_1
        True

        >>> set_1 == set_2
        False

        >>> set_1 < set_1
        False

        >>> set_1 < set_2
        False

        >>> set_1 <= set_1
        True

        >>> set_1 <= set_2
        False

        >>> set_1 > set_1
        False

        >>> set_1 > set_2
        False

        >>> set_1 >= set_1
        True

        >>> set_1 >= set_2
        False

    ..  container:: example

        Copy:

        >>> import copy
        >>> set_1_copy = copy.copy(set_1)
        >>> set_1_copy
        PitchSet([-26, -2.5, -1.5, 6, 7])

        >>> set_1 == set_1_copy
        True

    ..  container:: example

        Empty set:

        >>> set_ = abjad.PitchSet()
        >>> set_
        PitchSet()

        >>> str(set_)
        '{}'

        >>> len(set_)
        0

        >>> bool(set_)
        False

    """

    def __new__(class_, argument=()):
        argument = [_pitch.NumberedPitch(_) for _ in argument]
        argument.sort()
        self = frozenset.__new__(class_, argument)
        return self

    @classmethod
    def _wrap_methods(class_, names):
        def closure(name):
            def inner(self, *arguments):
                result = getattr(super(class_, self), name)(*arguments)
                result = PitchSet(result)
                return result

            inner.fn_name = name
            setattr(class_, name, inner)

        for name in names:
            closure(name)

    def __repr__(self):
        """
        Gets repr.
        """
        if self:
            numbers = [_.number for _ in sorted(self)]
            string = f"{type(self).__name__}({numbers!r})"
        else:
            string = f"{type(self).__name__}()"
        return string

    def __str__(self) -> str:
        """
        Gets string.
        """
        string = ", ".join([str(_.number) for _ in sorted(self)])
        return f"{{{string}}}"


collections.abc.Sequence.register(PitchSet)


PitchSet._wrap_methods(
    [
        "__and__",
        "__or__",
        "__sub__",
        "__xor__",
        "difference",
        "intersection",
        "symmetric_difference",
        "union",
    ]
)


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
        TwelveToneRow(items=(NumberedPitchClass(1), NumberedPitchClass(11), NumberedPitchClass(9), NumberedPitchClass(3), NumberedPitchClass(6), NumberedPitchClass(7), NumberedPitchClass(5), NumberedPitchClass(4), NumberedPitchClass(10), NumberedPitchClass(2), NumberedPitchClass(8), NumberedPitchClass(0)))

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

            >>> segment = abjad.PitchClassSegment([-2, -1, 6, 7, -1, 7])
            >>> lilypond_file = abjad.illustrate(segment)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  doctest::

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

            >>> row_ = abjad.TwelveToneRow([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
            >>> segment = row_(segment)
            >>> segment
            PitchClassSegment([4, 11, 5, 3, 11, 3])

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
            return PitchClassSegment(item)
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
        return PitchClassSegment(self.items) * argument

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
        return PitchClassSegment(self.items) * argument

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
        segment = PitchClassSegment(segment)
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
            segment = PitchClassSegment(segment)
            return segment
    candidates.sort(key=lambda x: x[0])
    segment = candidates[0]
    segment = PitchClassSegment(segment)
    return segment


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


def voice_horizontally(
    pcs: typing.Sequence[_pitch.NamedPitchClass],
    initial_octave: _pitch.Octave = _pitch.Octave(4),
) -> tuple[_pitch.NamedPitch, ...]:
    r"""
    Voices named ``pcs`` with each pitch as close to the previous pitch as possible.

    ..  container:: example

        >>> pcs = [abjad.NamedPitchClass(_) for _ in "c b d e f g e b a c".split()]
        >>> pitches = abjad.pcollections.voice_horizontally(pcs)
        >>> staff = abjad.Staff([abjad.Note(_, (1, 8)) for _ in pitches])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                b8
                d'8
                e'8
                f'8
                g'8
                e'8
                b8
                a8
                c'8
            }

    """
    assert all(isinstance(_, _pitch.NamedPitchClass) for _ in pcs), repr(pcs)
    assert isinstance(initial_octave, _pitch.Octave), repr(initial_octave)
    pitches = []
    if pcs:
        pc = pcs[0]
        pitch = _pitch.NamedPitch((pc.name, initial_octave))
        pitches.append(pitch)
        for pc in pcs[1:]:
            number = _pitch.NamedPitch((pc.name, initial_octave)).number
            semitones = abs((number - pitches[-1].number))
            while 6 < semitones:
                if number < pitches[-1].number:
                    number += 12
                else:
                    number -= 12
                semitones = abs((number - pitches[-1].number))
            pitch = _pitch.NamedPitch(number)
            pitches.append(pitch)
    return tuple(pitches)


def voice_vertically(
    pcs: typing.Sequence[_pitch.NamedPitchClass],
    initial_octave: _pitch.Octave = _pitch.Octave(4),
) -> tuple[_pitch.NamedPitch, ...]:
    r"""
    Voices named ``pcs`` with each pitch not lower than the previous.

    ..  container:: example

        >>> pcs = [abjad.NamedPitchClass(_) for _ in "c ef g bf d f af".split()]
        >>> pitches = abjad.pcollections.voice_vertically(pcs)
        >>> staff = abjad.Staff([abjad.Note(_, (1, 8)) for _ in pitches])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                ef'8
                g'8
                bf'8
                d''8
                f''8
                af''8
            }

    """
    assert all(isinstance(_, _pitch.NamedPitchClass) for _ in pcs), repr(pcs)
    assert isinstance(initial_octave, _pitch.Octave), repr(initial_octave)
    pitches = []
    if pcs:
        pc = _pitch.NamedPitchClass(pcs[0])
        pitch = _pitch.NamedPitch((pc.name, initial_octave))
        pitches.append(pitch)
        for pc in pcs[1:]:
            pc = _pitch.NamedPitchClass(pc)
            pitch = _pitch.NamedPitch((pc.name, initial_octave))
            while pitch < pitches[-1]:
                pitch += 12
            pitches.append(pitch)
    return tuple(pitches)
