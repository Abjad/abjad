import collections
import numbers
import typing

from abjad import mathtools
from abjad import pitch as abjad_pitch
from abjad import typings
from abjad.mathtools import NonreducedFraction
from abjad.system.Tag import Tag
from abjad.utilities.Duration import Duration
from abjad.utilities.Sequence import Sequence

from .Chord import Chord
from .Leaf import Leaf
from .MultimeasureRest import MultimeasureRest
from .Note import Note
from .Rest import Rest
from .Selection import Selection
from .Skip import Skip


class LeafMaker(object):
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

            >>> abjad.f(staff)
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

            >>> abjad.f(staff)
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

            >>> abjad.f(staff)
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

            >>> abjad.f(staff)
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

            >>> abjad.f(staff)
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

            >>> abjad.f(staff)
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

            >>> abjad.f(staff)
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

            >>> abjad.f(staff)
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

            >>> abjad.f(staff)
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

            >>> abjad.f(staff)
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

            >>> abjad.f(staff)
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

            >>> abjad.f(staff)
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
        >>> leaf = abjad.inspect(staff).leaf(0)
        >>> abjad.attach(time_signature, leaf)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \tweak edge-height #'(0.7 . 0)
                \times 4/7 {
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

            >>> abjad.f(staff)
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

            >>> abjad.f(staff)
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

    _publish_storage_format = True

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
        from .Tuplet import Tuplet

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
            factors_ = mathtools.factors(duration_group[0].denominator)
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
                numerator = mathtools.greatest_power_of_two_less_equal(denominator)
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
            abjad_pitch.NamedPitch,
            abjad_pitch.NumberedPitch,
            abjad_pitch.PitchClass,
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
        from abjad.spanners import tie as abjad_tie

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
            denominator = mathtools.least_common_multiple(*denominators)
            forbidden_duration = NonreducedFraction(forbidden_duration)
            forbidden_duration = forbidden_duration.with_denominator(denominator)
            duration = NonreducedFraction(duration)
            duration = duration.with_denominator(denominator)
            forbidden_numerator = forbidden_duration.numerator
            assert forbidden_numerator % 2 == 0
            preferred_numerator = forbidden_numerator / 2
        # make written duration numerators
        numerators = []
        parts = mathtools.partition_integer_into_canonic_parts(duration.numerator)
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
                abjad_tie(result)
        return result

    @staticmethod
    def _partition_less_than_double(n, m):
        assert mathtools.is_positive_integer_equivalent_number(n)
        assert mathtools.is_positive_integer_equivalent_number(m)
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

                >>> abjad.f(staff)
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
