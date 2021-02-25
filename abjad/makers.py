import collections
import math
import numbers
import typing

from . import _inspect, exceptions
from . import math as _math
from . import typings
from .duration import Duration, Multiplier, NonreducedFraction
from .pitch.pitchclasses import PitchClass
from .pitch.pitches import NamedPitch, NumberedPitch
from .ratio import NonreducedRatio, Ratio
from .score import Chord, Leaf, MultimeasureRest, Note, Rest, Skip, Tuplet
from .select import Selection
from .sequence import Sequence
from .spanners import tie
from .tag import Tag


class LeafMaker:
    r"""
    Leaf-maker.

    ..  container:: example

        Integer and string elements in ``pitches`` result in notes:

        >>> maker = abjad.LeafMaker()
        >>> pitches = [2, 4, 'F#5', 'G#5']
        >>> duration = abjad.Duration(1, 4)
        >>> leaves = maker(pitches, duration)
        >>> staff = abjad.Staff(leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                d'4
                e'4
                fs''4
                gs''4
            }

    ..  container:: example

        Tuple elements in ``pitches`` result in chords:

        >>> maker = abjad.LeafMaker()
        >>> pitches = [(0, 2, 4), ('F#5', 'G#5', 'A#5')]
        >>> duration = abjad.Duration(1, 2)
        >>> leaves = maker(pitches, duration)
        >>> staff = abjad.Staff(leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <c' d' e'>2
                <fs'' gs'' as''>2
            }

    ..  container:: example

        None-valued elements in ``pitches`` result in rests:

        >>> maker = abjad.LeafMaker()
        >>> pitches = 4 * [None]
        >>> durations = [abjad.Duration(1, 4)]
        >>> leaves = maker(pitches, durations)
        >>> staff = abjad.Staff(leaves)
        >>> staff.lilypond_type = 'RhythmicStaff'
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new RhythmicStaff
            {
                r4
                r4
                r4
                r4
            }

    ..  container:: example

        You can mix and match values passed to ``pitches``:

        >>> maker = abjad.LeafMaker()
        >>> pitches = [(0, 2, 4), None, 'C#5', 'D#5']
        >>> durations = [abjad.Duration(1, 4)]
        >>> leaves = maker(pitches, durations)
        >>> staff = abjad.Staff(leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <c' d' e'>4
                r4
                cs''4
                ds''4
            }

    ..  container:: example

        Works with segments:

        >>> maker = abjad.LeafMaker()
        >>> pitches = abjad.PitchSegment("e'' ef'' d'' df'' c''")
        >>> durations = [abjad.Duration(1, 4)]
        >>> leaves = maker(pitches, durations)
        >>> staff = abjad.Staff(leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                e''4
                ef''4
                d''4
                df''4
                c''4
            }

    ..  container:: example

        Reads ``pitches`` cyclically when the length of ``pitches`` is less
        than the length of ``durations``:

        >>> maker = abjad.LeafMaker()
        >>> pitches = ['C5']
        >>> durations = 2 * [abjad.Duration(3, 8), abjad.Duration(1, 8)]
        >>> leaves = maker(pitches, durations)
        >>> staff = abjad.Staff(leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c''4.
                c''8
                c''4.
                c''8
            }

    ..  container:: example

        Reads ``durations`` cyclically when the length of ``durations`` is less
        than the length of ``pitches``:

        >>> maker = abjad.LeafMaker()
        >>> pitches = "c'' d'' e'' f''"
        >>> durations = [abjad.Duration(1, 4)]
        >>> leaves = maker(pitches, durations)
        >>> staff = abjad.Staff(leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c''4
                d''4
                e''4
                f''4
            }

    ..  container:: example

        Elements in ``durations`` with non-power-of-two denominators result in
        tuplet-nested leaves:

        >>> maker = abjad.LeafMaker()
        >>> pitches = ['D5']
        >>> durations = 3 * [abjad.Duration(1, 3)]
        >>> leaves = maker(pitches, durations)
        >>> staff = abjad.Staff(leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \times 2/3 {
                    d''2
                    d''2
                    d''2
                }
            }

    ..  container:: example

        Set ``increase_monotonic`` to false to return nonassignable
        durations tied from greatest to least:

        >>> maker = abjad.LeafMaker(increase_monotonic=False)
        >>> pitches = ['D#5']
        >>> durations = [abjad.Duration(13, 16)]
        >>> leaves = maker(pitches, durations)
        >>> staff = abjad.Staff(leaves)
        >>> time_signature = abjad.TimeSignature((13, 16))
        >>> abjad.attach(time_signature, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \time 13/16
                ds''2.
                ~
                ds''16
            }

    ..  container:: example

        Set ``increase_monotonic`` to true to return nonassignable
        durations tied from least to greatest:

        >>> maker = abjad.LeafMaker(increase_monotonic=True)
        >>> pitches = ['E5']
        >>> durations = [abjad.Duration(13, 16)]
        >>> leaves = maker(pitches, durations)
        >>> staff = abjad.Staff(leaves)
        >>> time_signature = abjad.TimeSignature((13, 16))
        >>> abjad.attach(time_signature, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \time 13/16
                e''16
                ~
                e''2.
            }

    ..  container:: example

        Set ``forbidden_note_duration`` to avoid notes greater than or equal
        to a certain written duration:

        >>> maker = abjad.LeafMaker(
        ...     forbidden_note_duration=abjad.Duration(1, 2),
        ...     )
        >>> pitches = "f' g'"
        >>> durations = [abjad.Duration(5, 8)]
        >>> leaves = maker(pitches, durations)
        >>> staff = abjad.Staff(leaves)
        >>> time_signature = abjad.TimeSignature((5, 4))
        >>> abjad.attach(time_signature, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \time 5/4
                f'4
                ~
                f'4
                ~
                f'8
                g'4
                ~
                g'4
                ~
                g'8
            }

    ..  container:: example

        You may set ``forbidden_note_duration`` and ``increase_monotonic``
        together:

        >>> maker = abjad.LeafMaker(
        ...     forbidden_note_duration=abjad.Duration(1, 2),
        ...     increase_monotonic=True,
        ...     )
        >>> pitches = "f' g'"
        >>> durations = [abjad.Duration(5, 8)]
        >>> leaves = maker(pitches, durations)
        >>> staff = abjad.Staff(leaves)
        >>> time_signature = abjad.TimeSignature((5, 4))
        >>> abjad.attach(time_signature, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \time 5/4
                f'8
                ~
                f'4
                ~
                f'4
                g'8
                ~
                g'4
                ~
                g'4
            }

    ..  container:: example

        Produces diminished tuplets:

        >>> maker = abjad.LeafMaker()
        >>> pitches = "f'"
        >>> durations = [abjad.Duration(5, 14)]
        >>> leaves = maker(pitches, durations)
        >>> staff = abjad.Staff(leaves)
        >>> time_signature = abjad.TimeSignature((5, 14))
        >>> leaf = abjad.get.leaf(staff, 0)
        >>> abjad.attach(time_signature, leaf)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tweak edge-height #'(0.7 . 0)
                \times 8/14 {
                    #(ly:expect-warning "strange time signature found")
                    \time 5/14
                    f'2
                    ~
                    f'8
                }
            }

        This is default behavior.

    ..  container:: example

        None-valued elements in ``pitches`` result in multimeasure rests when
        the multimeasure rest keyword is set:

        >>> maker = abjad.LeafMaker(use_multimeasure_rests=True)
        >>> pitches = [None]
        >>> durations = [abjad.Duration(3, 8), abjad.Duration(5, 8)]
        >>> leaves = maker(pitches, durations)
        >>> leaves
        Selection([MultimeasureRest('R1 * 3/8'), MultimeasureRest('R1 * 5/8')])

        >>> abjad.attach(abjad.TimeSignature((3, 8)), leaves[0])
        >>> abjad.attach(abjad.TimeSignature((5, 8)), leaves[1])
        >>> staff = abjad.Staff(leaves)
        >>> staff.lilypond_type = 'RhythmicStaff'
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new RhythmicStaff
            {
                \time 3/8
                R1 * 3/8
                \time 5/8
                R1 * 5/8
            }

    ..  container:: example

        Works with numbered pitch-class:

        >>> maker = abjad.LeafMaker()
        >>> pitches = [abjad.NumberedPitchClass(6)]
        >>> durations = [abjad.Duration(13, 16)]
        >>> leaves = maker(pitches, durations)
        >>> staff = abjad.Staff(leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                fs'2.
                ~
                fs'16
            }

    ..  container:: example

        Makes skips instead of rests:

        >>> maker = abjad.LeafMaker(skips_instead_of_rests=True)
        >>> pitches = [None]
        >>> durations = [abjad.Duration(13, 16)]
        >>> maker(pitches, durations)
        Selection([Skip('s2.'), Skip('s16')])

    Returns selection of leaves.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Makers"

    __slots__ = (
        "_increase_monotonic",
        "_forbidden_note_duration",
        "_forbidden_rest_duration",
        "_skips_instead_of_rests",
        "_tag",
        "_use_multimeasure_rests",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        increase_monotonic: bool = None,
        forbidden_note_duration: typings.DurationTyping = None,
        forbidden_rest_duration: typings.DurationTyping = None,
        skips_instead_of_rests: bool = None,
        tag: Tag = None,
        use_multimeasure_rests: bool = None,
    ) -> None:
        if increase_monotonic is not None:
            increase_monotonic = bool(increase_monotonic)
        self._increase_monotonic = increase_monotonic
        if forbidden_note_duration is None:
            forbidden_note_duration_ = None
        else:
            forbidden_note_duration_ = Duration(forbidden_note_duration)
        self._forbidden_note_duration = forbidden_note_duration_
        if forbidden_rest_duration is None:
            forbidden_rest_duration_ = None
        else:
            forbidden_rest_duration_ = Duration(forbidden_rest_duration)
        self._forbidden_rest_duration = forbidden_rest_duration_
        if skips_instead_of_rests is not None:
            skips_instead_of_rests = bool(skips_instead_of_rests)
        self._skips_instead_of_rests = skips_instead_of_rests
        if tag is not None:
            assert isinstance(tag, Tag), repr(tag)
        self._tag = tag
        if use_multimeasure_rests is not None:
            use_multimeasure_rests = bool(use_multimeasure_rests)
        self._use_multimeasure_rests = use_multimeasure_rests

    ### SPECIAL METHODS ###

    def __call__(self, pitches, durations) -> Selection:
        """
        Calls leaf-maker on ``pitches`` and ``durations``.

        Returns selection.
        """
        if isinstance(pitches, str):
            pitches = pitches.split()
        if not isinstance(pitches, collections.abc.Iterable):
            pitches = [pitches]
        if isinstance(durations, (numbers.Number, tuple)):
            durations = [durations]
        nonreduced_fractions = Sequence([NonreducedFraction(_) for _ in durations])
        size = max(len(nonreduced_fractions), len(pitches))
        nonreduced_fractions = nonreduced_fractions.repeat_to_length(size)
        pitches = Sequence(pitches).repeat_to_length(size)
        duration_groups = Duration._group_by_implied_prolation(nonreduced_fractions)
        result: typing.List[typing.Union[Tuplet, Leaf]] = []
        for duration_group in duration_groups:
            # get factors in denominator of duration group other than 1, 2.
            factors_ = _math.factors(duration_group[0].denominator)
            factors = set(factors_)
            factors.discard(1)
            factors.discard(2)
            current_pitches = pitches[0 : len(duration_group)]
            pitches = pitches[len(duration_group) :]
            if len(factors) == 0:
                for pitch, duration in zip(current_pitches, duration_group):
                    leaves = self._make_leaf_on_pitch(
                        pitch,
                        duration,
                        increase_monotonic=self.increase_monotonic,
                        forbidden_note_duration=self.forbidden_note_duration,
                        forbidden_rest_duration=self.forbidden_rest_duration,
                        skips_instead_of_rests=self.skips_instead_of_rests,
                        tag=self.tag,
                        use_multimeasure_rests=self.use_multimeasure_rests,
                    )
                    result.extend(leaves)
            else:
                # compute tuplet prolation
                denominator = duration_group[0].denominator
                numerator = _math.greatest_power_of_two_less_equal(denominator)
                multiplier = (numerator, denominator)
                ratio = 1 / Duration(*multiplier)
                duration_group = [
                    ratio * Duration(duration) for duration in duration_group
                ]
                # make tuplet leaves
                tuplet_leaves: typing.List[Leaf] = []
                for pitch, duration in zip(current_pitches, duration_group):
                    leaves = self._make_leaf_on_pitch(
                        pitch,
                        duration,
                        increase_monotonic=self.increase_monotonic,
                        skips_instead_of_rests=self.skips_instead_of_rests,
                        tag=self.tag,
                        use_multimeasure_rests=self.use_multimeasure_rests,
                    )
                    tuplet_leaves.extend(leaves)
                tuplet = Tuplet(multiplier, tuplet_leaves)
                result.append(tuplet)
        return Selection(result)

    ### PRIVATE METHODS ###

    @staticmethod
    def _make_leaf_on_pitch(
        pitch,
        duration,
        *,
        increase_monotonic=None,
        forbidden_note_duration=None,
        forbidden_rest_duration=None,
        skips_instead_of_rests=None,
        tag=None,
        use_multimeasure_rests=None,
    ):
        note_prototype = (
            numbers.Number,
            str,
            NamedPitch,
            NumberedPitch,
            PitchClass,
        )
        chord_prototype = (tuple, list)
        rest_prototype = (type(None),)
        if isinstance(pitch, note_prototype):
            leaves = LeafMaker._make_tied_leaf(
                Note,
                duration,
                increase_monotonic=increase_monotonic,
                forbidden_duration=forbidden_note_duration,
                pitches=pitch,
                tag=tag,
            )
        elif isinstance(pitch, chord_prototype):
            leaves = LeafMaker._make_tied_leaf(
                Chord,
                duration,
                increase_monotonic=increase_monotonic,
                forbidden_duration=forbidden_note_duration,
                pitches=pitch,
                tag=tag,
            )
        elif isinstance(pitch, rest_prototype) and skips_instead_of_rests:
            leaves = LeafMaker._make_tied_leaf(
                Skip,
                duration,
                increase_monotonic=increase_monotonic,
                forbidden_duration=forbidden_rest_duration,
                pitches=None,
                tag=tag,
            )
        elif isinstance(pitch, rest_prototype) and not use_multimeasure_rests:
            leaves = LeafMaker._make_tied_leaf(
                Rest,
                duration,
                increase_monotonic=increase_monotonic,
                forbidden_duration=forbidden_rest_duration,
                pitches=None,
                tag=tag,
            )
        elif isinstance(pitch, rest_prototype) and use_multimeasure_rests:
            multimeasure_rest = MultimeasureRest((1), tag=tag)
            multimeasure_rest.multiplier = duration
            leaves = (multimeasure_rest,)
        else:
            raise ValueError(f"unknown pitch: {pitch!r}.")
        return leaves

    @staticmethod
    def _make_tied_leaf(
        class_,
        duration,
        increase_monotonic=None,
        forbidden_duration=None,
        multiplier=None,
        pitches=None,
        tag=None,
        tie_parts=True,
    ):
        duration = Duration(duration)
        if forbidden_duration is not None:
            assert forbidden_duration.is_assignable
            assert forbidden_duration.numerator == 1
        # find preferred numerator of written durations if necessary
        if forbidden_duration is not None and forbidden_duration <= duration:
            denominators = [
                2 * forbidden_duration.denominator,
                duration.denominator,
            ]
            denominator = _math.least_common_multiple(*denominators)
            forbidden_duration = NonreducedFraction(forbidden_duration)
            forbidden_duration = forbidden_duration.with_denominator(denominator)
            duration = NonreducedFraction(duration)
            duration = duration.with_denominator(denominator)
            forbidden_numerator = forbidden_duration.numerator
            assert forbidden_numerator % 2 == 0
            preferred_numerator = forbidden_numerator / 2
        # make written duration numerators
        numerators = []
        parts = _math.partition_integer_into_canonic_parts(duration.numerator)
        if forbidden_duration is not None and forbidden_duration <= duration:
            for part in parts:
                if forbidden_numerator <= part:
                    better_parts = LeafMaker._partition_less_than_double(
                        part, preferred_numerator
                    )
                    numerators.extend(better_parts)
                else:
                    numerators.append(part)
        else:
            numerators = parts
        # reverse numerators if necessary
        if increase_monotonic:
            numerators = list(reversed(numerators))
        # make one leaf per written duration
        result = []
        for numerator in numerators:
            written_duration = Duration(numerator, duration.denominator)
            if pitches is not None:
                arguments = (pitches, written_duration)
            else:
                arguments = (written_duration,)
            result.append(class_(*arguments, multiplier=multiplier, tag=tag))
        result = Selection(result)
        # tie if required
        if tie_parts and 1 < len(result):
            if not issubclass(class_, (Rest, Skip)):
                tie(result)
        return result

    @staticmethod
    def _partition_less_than_double(n, m):
        assert _math.is_positive_integer_equivalent_number(n)
        assert _math.is_positive_integer_equivalent_number(m)
        n, m = int(n), int(m)
        result = []
        current_value = n
        double_m = 2 * m
        while double_m <= current_value:
            result.append(m)
            current_value -= m
        result.append(current_value)
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def forbidden_note_duration(self) -> typing.Optional[Duration]:
        """
        Gets forbidden written duration.
        """
        return self._forbidden_note_duration

    @property
    def forbidden_rest_duration(self) -> typing.Optional[Duration]:
        """
        Gets forbidden written duration.
        """
        return self._forbidden_rest_duration

    @property
    def increase_monotonic(self) -> typing.Optional[bool]:
        """
        Is true when durations increase monotonically.
        """
        return self._increase_monotonic

    @property
    def skips_instead_of_rests(self) -> typing.Optional[bool]:
        """
        Is true when skips appear in place of rests.
        """
        return self._skips_instead_of_rests

    @property
    def tag(self) -> typing.Optional[Tag]:
        r"""
        Gets tag.

        ..  container:: example

            Integer and string elements in ``pitches`` result in notes:

            >>> maker = abjad.LeafMaker(tag=abjad.Tag("leaf_maker"))
            >>> pitches = [2, 4, 'F#5', 'G#5']
            >>> duration = abjad.Duration(1, 4)
            >>> leaves = maker(pitches, duration)
            >>> staff = abjad.Staff(leaves)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff, tags=True)
                >>> print(string)
                \new Staff
                {
                    d'4 %! leaf_maker
                    e'4 %! leaf_maker
                    fs''4 %! leaf_maker
                    gs''4 %! leaf_maker
                }

        """
        return self._tag

    @property
    def use_multimeasure_rests(self) -> typing.Optional[bool]:
        """
        Is true when rests are multimeasure.
        """
        return self._use_multimeasure_rests


class NoteMaker:
    r"""
    Note-maker.

    Makes notes according to ``pitches`` and ``durations``.

    ..  container:: example

        Cycles through ``pitches`` when the length of ``pitches`` is less than
        the length of ``durations``:

        >>> maker = abjad.NoteMaker()
        >>> notes = maker([0], [(1, 16), (1, 8), (1, 8)])
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'16
                c'8
                c'8
            }

    ..  container:: example

        Cycles through ``durations`` when the length of ``durations`` is less
        than the length of ``pitches``:

        >>> maker = abjad.NoteMaker()
        >>> notes = maker(
        ...     [0, 2, 4, 5, 7],
        ...     [(1, 16), (1, 8), (1, 8)],
        ...     )
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'16
                d'8
                e'8
                f'16
                g'8
            }

    ..  container:: example

        Creates ad hoc tuplets for nonassignable durations:

        >>> maker = abjad.NoteMaker()
        >>> notes = maker([0], [(1, 16), (1, 12), (1, 8)])
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'16
                \tweak edge-height #'(0.7 . 0)
                \times 2/3 {
                    c'8
                }
                c'8
            }

    ..  container:: example

        Set ``increase_monotonic=False`` to express tied values in decreasing
        duration:

        >>> maker = abjad.NoteMaker(increase_monotonic=False)
        >>> notes = maker([0], [(13, 16)])
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'2.
                ~
                c'16
            }

    ..  container:: example

        Set ``increase_monotonic=True`` to express tied values in increasing
        duration:

        >>> maker = abjad.NoteMaker(increase_monotonic=True)
        >>> notes = maker([0], [(13, 16)])
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'16
                ~
                c'2.
            }

    ..  container:: example

        Works with pitch segments:

        >>> maker = abjad.NoteMaker()
        >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
        >>> notes = maker(segment, [(1, 8)])
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                bf8
                bqf8
                fs'8
                g'8
                bqf8
                g'8
            }

    Set ``pitches`` to a single pitch or a sequence of pitches.

    Set ``durations`` to a single duration or a list of durations.

    Returns selection.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Makers"

    __slots__ = ("_increase_monotonic", "_tag")

    ### INITIALIZER ###

    def __init__(self, *, increase_monotonic: bool = None, tag: Tag = None) -> None:
        if increase_monotonic is not None:
            increase_monotonic = bool(increase_monotonic)
        self._increase_monotonic = increase_monotonic
        if tag is not None:
            assert isinstance(tag, Tag), repr(tag)
        self._tag = tag

    ### SPECIAL METHODS ###

    def __call__(self, pitches, durations) -> Selection:
        """
        Calls note-maker on ``pitches`` and ``durations``.
        """
        if isinstance(pitches, str):
            pitches = pitches.split()
        if not isinstance(pitches, collections.abc.Iterable):
            pitches = [pitches]
        if isinstance(durations, (numbers.Number, tuple)):
            durations = [durations]
        nonreduced_fractions = Sequence([NonreducedFraction(_) for _ in durations])
        size = max(len(nonreduced_fractions), len(pitches))
        nonreduced_fractions = nonreduced_fractions.repeat_to_length(size)
        pitches = Sequence(pitches).repeat_to_length(size)
        durations = Duration._group_by_implied_prolation(nonreduced_fractions)
        result: typing.List[typing.Union[Note, Tuplet]] = []
        for duration in durations:
            # get factors in denominator of duration group duration not 1 or 2
            factors = set(_math.factors(duration[0].denominator))
            factors.discard(1)
            factors.discard(2)
            ps = pitches[0 : len(duration)]
            pitches = pitches[len(duration) :]
            if len(factors) == 0:
                result.extend(
                    self._make_unprolated_notes(
                        ps,
                        duration,
                        increase_monotonic=self.increase_monotonic,
                        tag=self.tag,
                    )
                )
            else:
                # compute prolation
                denominator = duration[0].denominator
                numerator = _math.greatest_power_of_two_less_equal(denominator)
                multiplier = Multiplier(numerator, denominator)
                ratio = multiplier.reciprocal
                duration = [ratio * Duration(d) for d in duration]
                ns = self._make_unprolated_notes(
                    ps,
                    duration,
                    increase_monotonic=self.increase_monotonic,
                    tag=self.tag,
                )
                tuplet = Tuplet(multiplier, ns)
                result.append(tuplet)
        return Selection(result)

    ### PRIVATE METHODS ###

    @staticmethod
    def _make_unprolated_notes(pitches, durations, increase_monotonic=None, tag=None):
        assert len(pitches) == len(durations)
        result = []
        for pitch, duration in zip(pitches, durations):
            result.extend(
                LeafMaker._make_tied_leaf(
                    Note,
                    duration,
                    pitches=pitch,
                    increase_monotonic=increase_monotonic,
                    tag=tag,
                )
            )
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def increase_monotonic(self) -> typing.Optional[bool]:
        """
        Is true when durations increase monotonically.
        """
        return self._increase_monotonic

    @property
    def tag(self) -> typing.Optional[Tag]:
        r"""
        Gets tag.

        ..  container:: example

            >>> maker = abjad.NoteMaker(tag=abjad.Tag('note_maker'))
            >>> notes = maker([0], [(1, 16), (1, 8), (1, 8)])
            >>> staff = abjad.Staff(notes)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff, tags=True)
                >>> print(string)
                \new Staff
                {
                    c'16 %! note_maker
                    c'8 %! note_maker
                    c'8 %! note_maker
                }

        """
        return self._tag


### FUNCTIONS ###


def tuplet_from_duration_and_ratio(
    duration, ratio, *, increase_monotonic: bool = None, tag: Tag = None
) -> "Tuplet":
    r"""
    Makes tuplet from ``duration`` and ``ratio``.

    ..  container:: example

        Makes tupletted leaves strictly without dots when all
        ``ratio`` equal ``1``:

        >>> tuplet = abjad.makers.tuplet_from_duration_and_ratio(
        ...     abjad.Duration(3, 16),
        ...     abjad.Ratio((1, 1, 1, -1, -1)),
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \times 4/5 {
                \time 3/16
                c'32.
                c'32.
                c'32.
                r32.
                r32.
            }

        Allows tupletted leaves to return with dots when some ``ratio``
        do not equal ``1``:

        >>> tuplet = abjad.makers.tuplet_from_duration_and_ratio(
        ...     abjad.Duration(3, 16),
        ...     abjad.Ratio((1, -2, -2, 3, 3)),
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \times 6/11 {
                \time 3/16
                c'32
                r16
                r16
                c'16.
                c'16.
            }

        Interprets nonassignable ``ratio`` according to
        ``increase_monotonic``:

        >>> tuplet = abjad.makers.tuplet_from_duration_and_ratio(
        ...     abjad.Duration(3, 16),
        ...     abjad.Ratio((5, -1, 5)),
        ...     increase_monotonic=True,
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \times 8/11 {
                \time 3/16
                c'16...
                r64.
                c'16...
            }

    ..  container:: example

        Makes augmented tuplet from ``duration`` and ``ratio`` and
        encourages dots:

        >>> tuplet = abjad.makers.tuplet_from_duration_and_ratio(
        ...     abjad.Duration(3, 16),
        ...     abjad.Ratio((1, 1, 1, -1, -1)),
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \times 4/5 {
                \time 3/16
                c'32.
                c'32.
                c'32.
                r32.
                r32.
            }

        Interprets nonassignable ``ratio`` according to
        ``increase_monotonic``:

        >>> tuplet = abjad.makers.tuplet_from_duration_and_ratio(
        ...     abjad.Duration(3, 16),
        ...     abjad.Ratio((5, -1, 5)),
        ...     increase_monotonic=True,
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \times 8/11 {
                \time 3/16
                c'16...
                r64.
                c'16...
            }

    ..  container:: example

        Makes diminished tuplet from ``duration`` and nonzero integer
        ``ratio``.

        Makes tupletted leaves strictly without dots when all
        ``ratio`` equal ``1``:

        >>> tuplet = abjad.makers.tuplet_from_duration_and_ratio(
        ...     abjad.Duration(3, 16),
        ...     abjad.Ratio((1, 1, 1, -1, -1)),
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \times 4/5 {
                \time 3/16
                c'32.
                c'32.
                c'32.
                r32.
                r32.
            }

        Allows tupletted leaves to return with dots when some ``ratio``
        do not equal ``1``:

        >>> tuplet = abjad.makers.tuplet_from_duration_and_ratio(
        ...     abjad.Duration(3, 16),
        ...     abjad.Ratio((1, -2, -2, 3, 3)),
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \times 6/11 {
                \time 3/16
                c'32
                r16
                r16
                c'16.
                c'16.
            }

        Interprets nonassignable ``ratio`` according to
        ``increase_monotonic``:

        >>> tuplet = abjad.makers.tuplet_from_duration_and_ratio(
        ...     abjad.Duration(3, 16),
        ...     abjad.Ratio((5, -1, 5)),
        ...     increase_monotonic=True,
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \times 8/11 {
                \time 3/16
                c'16...
                r64.
                c'16...
            }

    ..  container:: example

        Makes diminished tuplet from ``duration`` and ``ratio`` and
        encourages dots:

        >>> tuplet = abjad.makers.tuplet_from_duration_and_ratio(
        ...     abjad.Duration(3, 16),
        ...     abjad.Ratio((1, 1, 1, -1, -1)),
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type = 'RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \times 4/5 {
                \time 3/16
                c'32.
                c'32.
                c'32.
                r32.
                r32.
            }

        Interprets nonassignable ``ratio`` according to ``direction``:

        >>> tuplet = abjad.makers.tuplet_from_duration_and_ratio(
        ...     abjad.Duration(3, 16),
        ...     abjad.Ratio((5, -1, 5)),
        ...     increase_monotonic=True,
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \times 8/11 {
                \time 3/16
                c'16...
                r64.
                c'16...
            }

    Reduces ``ratio`` relative to each other.

    Interprets negative ``ratio`` as rests.
    """
    duration = Duration(duration)
    ratio = Ratio(ratio)
    basic_prolated_duration = duration / _math.weight(ratio.numbers)
    basic_written_duration = basic_prolated_duration.equal_or_greater_assignable
    written_durations = [x * basic_written_duration for x in ratio.numbers]
    leaf_maker = LeafMaker(increase_monotonic=increase_monotonic, tag=tag)
    try:
        notes = [
            Note(0, x, tag=tag) if 0 < x else Rest(abs(x), tag=tag)
            for x in written_durations
        ]
    except exceptions.AssignabilityError:
        denominator = duration.denominator
        note_durations = [Duration(x, denominator) for x in ratio.numbers]
        pitches = [None if note_duration < 0 else 0 for note_duration in note_durations]
        leaf_durations = [abs(note_duration) for note_duration in note_durations]
        notes = list(leaf_maker(pitches, leaf_durations))
    tuplet = Tuplet.from_duration(duration, notes, tag=tag)
    tuplet.normalize_multiplier()
    return tuplet


def tuplet_from_leaf_and_ratio(
    leaf: Leaf, ratio: typing.Union[typing.List, Ratio]
) -> "Tuplet":
    r"""
    Makes tuplet from ``leaf`` and ``ratio``.

    >>> note = abjad.Note("c'8.")

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(
        ...     note,
        ...     abjad.Ratio((1,)),
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \times 1/1 {
                \time 3/16
                c'8.
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(
        ...     note,
        ...     [1, 2],
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \times 1/1 {
                \time 3/16
                c'16
                c'8
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(
        ...     note,
        ...     abjad.Ratio((1, 2, 2)),
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \times 4/5 {
                \time 3/16
                c'32.
                c'16.
                c'16.
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(
        ...     note,
        ...     [1, 2, 2, 3],
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \times 6/8 {
                \time 3/16
                c'32
                c'16
                c'16
                c'16.
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(
        ...     note,
        ...     [1, 2, 2, 3, 3],
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \times 6/11 {
                \time 3/16
                c'32
                c'16
                c'16
                c'16.
                c'16.
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(
        ...     note,
        ...     abjad.Ratio((1, 2, 2, 3, 3, 4)),
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \times 4/5 {
                \time 3/16
                c'64
                c'32
                c'32
                c'32.
                c'32.
                c'16
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(
        ...     note,
        ...     [1],
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \times 1/1 {
                \time 3/16
                c'8.
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(
        ...     note,
        ...     [1, 2],
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \times 1/1 {
                \time 3/16
                c'16
                c'8
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(
        ...     note,
        ...     [1, 2, 2],
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \times 4/5 {
                \time 3/16
                c'32.
                c'16.
                c'16.
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(
        ...     note,
        ...     [1, 2, 2, 3],
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \times 6/8 {
                \time 3/16
                c'32
                c'16
                c'16
                c'16.
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(
        ...     note,
        ...     [1, 2, 2, 3, 3],
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \times 6/11 {
                \time 3/16
                c'32
                c'16
                c'16
                c'16.
                c'16.
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(
        ...     note,
        ...     [1, 2, 2, 3, 3, 4],
        ...     )
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \times 4/5 {
                \time 3/16
                c'64
                c'32
                c'32
                c'32.
                c'32.
                c'16
            }

    Returns tuplet.
    """
    proportions = Ratio(ratio)
    target_duration = leaf.written_duration
    basic_prolated_duration = target_duration / sum(proportions.numbers)
    basic_written_duration = basic_prolated_duration.equal_or_greater_assignable
    written_durations = [_ * basic_written_duration for _ in proportions.numbers]
    maker = NoteMaker()
    try:
        notes = [Note(0, x) for x in written_durations]
    except exceptions.AssignabilityError:
        denominator = target_duration.denominator
        note_durations = [Duration(_, denominator) for _ in proportions.numbers]
        notes = list(maker(0, note_durations))
    contents_duration = _inspect._get_duration(notes)
    multiplier = target_duration / contents_duration
    tuplet = Tuplet(multiplier, notes)
    tuplet.normalize_multiplier()
    return tuplet


def tuplet_from_ratio_and_pair(
    ratio: typing.Union[typing.Tuple, NonreducedRatio],
    fraction: typing.Union[typing.Tuple, NonreducedFraction],
    *,
    tag: Tag = None,
) -> "Tuplet":
    r"""
    Makes tuplet from nonreduced ``ratio`` and nonreduced ``fraction``.

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_ratio_and_pair(
        ...     abjad.NonreducedRatio((1,)),
        ...     abjad.NonreducedFraction(7, 16),
        ...     )
        >>> abjad.attach(abjad.TimeSignature((7, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \times 1/1 {
                \time 7/16
                c'4..
            }

        >>> tuplet = abjad.makers.tuplet_from_ratio_and_pair(
        ...     abjad.NonreducedRatio((1, 2)),
        ...     abjad.NonreducedFraction(7, 16),
        ...     )
        >>> abjad.attach(abjad.TimeSignature((7, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \times 7/6 {
                \time 7/16
                c'8
                c'4
            }

        >>> tuplet = abjad.makers.tuplet_from_ratio_and_pair(
        ...     abjad.NonreducedRatio((1, 2, 4)),
        ...     abjad.NonreducedFraction(7, 16),
        ...     )
        >>> abjad.attach(abjad.TimeSignature((7, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \times 1/1 {
                \time 7/16
                c'16
                c'8
                c'4
            }

        >>> tuplet = abjad.makers.tuplet_from_ratio_and_pair(
        ...     abjad.NonreducedRatio((1, 2, 4, 1)),
        ...     abjad.NonreducedFraction(7, 16),
        ...     )
        >>> abjad.attach(abjad.TimeSignature((7, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \times 7/8 {
                \time 7/16
                c'16
                c'8
                c'4
                c'16
            }

        >>> tuplet = abjad.makers.tuplet_from_ratio_and_pair(
        ...     abjad.NonreducedRatio((1, 2, 4, 1, 2)),
        ...     abjad.NonreducedFraction(7, 16),
        ...     )
        >>> abjad.attach(abjad.TimeSignature((7, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \times 7/10 {
                \time 7/16
                c'16
                c'8
                c'4
                c'16
                c'8
            }

        >>> tuplet = abjad.makers.tuplet_from_ratio_and_pair(
        ...     abjad.NonreducedRatio((1, 2, 4, 1, 2, 4)),
        ...     abjad.NonreducedFraction(7, 16),
        ...     )
        >>> abjad.attach(abjad.TimeSignature((7, 16)), tuplet[0])
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type='RhythmicStaff',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \times 1/2 {
                \time 7/16
                c'16
                c'8
                c'4
                c'16
                c'8
                c'4
            }

    Interprets ``d`` as tuplet denominator.
    """
    ratio = NonreducedRatio(ratio)
    if isinstance(fraction, tuple):
        fraction = NonreducedFraction(*fraction)
    numerator = fraction.numerator
    denominator = fraction.denominator
    duration = Duration(fraction)
    if len(ratio.numbers) == 1:
        if 0 < ratio.numbers[0]:
            try:
                note = Note(0, duration, tag=tag)
                duration = note._get_duration()
                tuplet = Tuplet.from_duration(duration, [note], tag=tag)
                return tuplet
            except exceptions.AssignabilityError:
                note_maker = NoteMaker(tag=tag)
                notes = note_maker(0, duration)
                duration = _inspect._get_duration(notes)
                return Tuplet.from_duration(duration, notes, tag=tag)
        elif ratio.numbers[0] < 0:
            try:
                rest = Rest(duration, tag=tag)
                duration = rest._get_duration()
                return Tuplet.from_duration(duration, [rest], tag=tag)
            except exceptions.AssignabilityError:
                leaf_maker = LeafMaker(tag=tag)
                rests = leaf_maker([None], duration)
                duration = _inspect._get_duration(rests)
                return Tuplet.from_duration(duration, rests, tag=tag)
        else:
            raise ValueError("no divide zero values.")
    else:
        exponent = int(
            math.log(_math.weight(ratio.numbers), 2) - math.log(numerator, 2)
        )
        denominator = int(denominator * 2 ** exponent)
        components: typing.List[typing.Union[Note, Rest]] = []
        for x in ratio.numbers:
            if not x:
                raise ValueError("no divide zero values.")
            if 0 < x:
                try:
                    note = Note(0, (x, denominator), tag=tag)
                    components.append(note)
                except exceptions.AssignabilityError:
                    maker = NoteMaker(tag=tag)
                    notes = maker(0, (x, denominator))
                    components.extend(notes)
            else:
                rest = Rest((-x, denominator), tag=tag)
                components.append(rest)
        return Tuplet.from_duration(duration, components, tag=tag)
