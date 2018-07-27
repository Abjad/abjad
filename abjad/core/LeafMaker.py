import collections
import numbers
from abjad.system.AbjadValueObject import AbjadValueObject


class LeafMaker(AbjadValueObject):
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

        Set ``decrease_monotonic`` to true to return nonassignable
        durations tied from greatest to least:

        >>> maker = abjad.LeafMaker()
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

        Set ``decrease_monotonic`` to false to return nonassignable
        durations tied from least to greatest:

        >>> maker = abjad.LeafMaker(decrease_monotonic=False)
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

        Set ``forbidden_duration`` to avoid notes greater than or equal
        to a certain written duration:

        >>> maker = abjad.LeafMaker(
        ...     forbidden_duration=abjad.Duration(1, 2),
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

        You may set ``forbidden_duration`` and ``decrease_monotonic`` together:

        >>> maker = abjad.LeafMaker(
        ...     forbidden_duration=abjad.Duration(1, 2),
        ...     decrease_monotonic=False,
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

        >>> staff = abjad.Staff([
        ...     abjad.Measure((3, 8), [leaves[0]]),
        ...     abjad.Measure((5, 8), [leaves[1]]),
        ...     ])
        >>> staff.lilypond_type = 'RhythmicStaff'
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new RhythmicStaff
            {
                {   % measure
                    \time 3/8
                    R1 * 3/8
                }   % measure
                {   % measure
                    \time 5/8
                    R1 * 5/8
                }   % measure
            }

    ..  container:: example

        Uses repeat ties:

        >>> maker = abjad.LeafMaker(repeat_ties=True)
        >>> pitches = [0]
        >>> durations = [abjad.Duration(13, 16)]
        >>> leaves = maker(pitches, durations)
        >>> staff = abjad.Staff(leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'2.
                c'16
                \repeatTie
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

    __documentation_section__ = 'Makers'

    __slots__ = (
        '_decrease_monotonic',
        '_forbidden_duration',
        '_metrical_hierarchy',
        '_skips_instead_of_rests',
        '_repeat_ties',
        '_use_multimeasure_rests',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        decrease_monotonic=True,
        forbidden_duration=None,
        metrical_hierarchy=None,
        skips_instead_of_rests=False,
        repeat_ties=False,
        use_multimeasure_rests=False,
        ):
        self._decrease_monotonic = decrease_monotonic
        self._forbidden_duration = forbidden_duration
        self._metrical_hierarchy = metrical_hierarchy
        self._skips_instead_of_rests = skips_instead_of_rests
        self._repeat_ties = repeat_ties
        self._use_multimeasure_rests = use_multimeasure_rests

    ### SPECIAL METHODS ###

    def __call__(self, pitches, durations):
        """
        Calls leaf-maker on ``pitches`` and ``durations``.

        Returns selection.
        """
        import abjad
        if isinstance(pitches, str):
            pitches = pitches.split()
        if not isinstance(pitches, collections.Iterable):
            pitches = [pitches]
        if isinstance(durations, (numbers.Number, tuple)):
            durations = [durations]
        nonreduced_fractions = [abjad.NonreducedFraction(_) for _ in durations]
        size = max(len(nonreduced_fractions), len(pitches))
        nonreduced_fractions = abjad.sequence(nonreduced_fractions)
        nonreduced_fractions = nonreduced_fractions.repeat_to_length(size)
        pitches = abjad.sequence(pitches).repeat_to_length(size)
        Duration = abjad.Duration
        duration_groups = Duration._group_by_implied_prolation(
            nonreduced_fractions
            )
        result = []
        for duration_group in duration_groups:
            # get factors in denominator of duration group other than 1, 2.
            factors = abjad.mathtools.factors(duration_group[0].denominator)
            factors = set(factors)
            factors.discard(1)
            factors.discard(2)
            current_pitches = pitches[0:len(duration_group)]
            pitches = pitches[len(duration_group):]
            if len(factors) == 0:
                for pitch, duration in zip(current_pitches, duration_group):
                    leaves = self._make_leaf_on_pitch(
                        pitch,
                        duration,
                        decrease_monotonic=self.decrease_monotonic,
                        forbidden_duration=self.forbidden_duration,
                        skips_instead_of_rests=self.skips_instead_of_rests,
                        use_multimeasure_rests=self.use_multimeasure_rests,
                        repeat_ties=self.repeat_ties,
                        )
                    result.extend(leaves)
            else:
                # compute tuplet prolation
                denominator = duration_group[0].denominator
                numerator = abjad.mathtools.greatest_power_of_two_less_equal(
                    denominator)
                multiplier = (numerator, denominator)
                ratio = 1 / abjad.Duration(*multiplier)
                duration_group = [
                    ratio * abjad.Duration(duration)
                    for duration in duration_group
                    ]
                # make tuplet leaves
                tuplet_leaves = []
                for pitch, duration in zip(current_pitches, duration_group):
                    leaves = self._make_leaf_on_pitch(
                        pitch,
                        duration,
                        decrease_monotonic=self.decrease_monotonic,
                        skips_instead_of_rests=self.skips_instead_of_rests,
                        use_multimeasure_rests=self.use_multimeasure_rests,
                        repeat_ties=self.repeat_ties,
                        )
                    tuplet_leaves.extend(leaves)
                tuplet = abjad.Tuplet(multiplier, tuplet_leaves)
                result.append(tuplet)
        return abjad.select(result)

    ### PRIVATE METHODS ###

    @staticmethod
    def _make_leaf_on_pitch(
        pitch,
        duration,
        decrease_monotonic=True,
        forbidden_duration=None,
        skips_instead_of_rests=False,
        use_multimeasure_rests=False,
        repeat_ties=False,
        ):
        import abjad
        note_prototype = (
            numbers.Number,
            str,
            abjad.NamedPitch,
            abjad.NumberedPitch,
            abjad.PitchClass,
            )
        chord_prototype = (tuple, list)
        rest_prototype = (type(None),)
        if isinstance(pitch, note_prototype):
            leaves = LeafMaker._make_tied_leaf(
                abjad.Note,
                duration,
                decrease_monotonic=decrease_monotonic,
                forbidden_duration=forbidden_duration,
                pitches=pitch,
                repeat_ties=repeat_ties,
                )
        elif isinstance(pitch, chord_prototype):
            leaves = LeafMaker._make_tied_leaf(
                abjad.Chord,
                duration,
                decrease_monotonic=decrease_monotonic,
                forbidden_duration=forbidden_duration,
                pitches=pitch,
                repeat_ties=repeat_ties,
                )
        elif isinstance(pitch, rest_prototype) and skips_instead_of_rests:
            leaves = LeafMaker._make_tied_leaf(
                abjad.Skip,
                duration,
                decrease_monotonic=decrease_monotonic,
                forbidden_duration=forbidden_duration,
                pitches=None,
                repeat_ties=repeat_ties,
                )
        elif isinstance(pitch, rest_prototype) and not use_multimeasure_rests:
            leaves = LeafMaker._make_tied_leaf(
                abjad.Rest,
                duration,
                decrease_monotonic=decrease_monotonic,
                forbidden_duration=forbidden_duration,
                pitches=None,
                repeat_ties=repeat_ties,
                )
        elif isinstance(pitch, rest_prototype) and use_multimeasure_rests:
            multimeasure_rest = abjad.MultimeasureRest((1))
            multiplier = abjad.Multiplier(duration)
            abjad.attach(multiplier, multimeasure_rest)
            leaves = (
                multimeasure_rest,
                )
        else:
            message = 'unknown pitch: {!r}.'
            message = message.format(pitch)
            raise ValueError(message)
        return leaves

    @staticmethod
    def _make_tied_leaf(
        class_,
        duration,
        decrease_monotonic=True,
        forbidden_duration=None,
        pitches=None,
        tie_parts=True,
        repeat_ties=False,
        ):
        import abjad
        # check input
        duration = abjad.Duration(duration)
        if forbidden_duration is not None:
            forbidden_duration = abjad.Duration(forbidden_duration)
            assert forbidden_duration.is_assignable
            assert forbidden_duration.numerator == 1
        # find preferred numerator of written durations if necessary
        if (forbidden_duration is not None and
            forbidden_duration <= duration):
            denominators = [
                2 * forbidden_duration.denominator,
                duration.denominator,
                ]
            denominator = abjad.mathtools.least_common_multiple(*denominators)
            forbidden_duration = abjad.NonreducedFraction(forbidden_duration)
            forbidden_duration = forbidden_duration.with_denominator(
                denominator)
            duration = abjad.NonreducedFraction(duration)
            duration = duration.with_denominator(denominator)
            forbidden_numerator = forbidden_duration.numerator
            assert forbidden_numerator % 2 == 0
            preferred_numerator = forbidden_numerator / 2
        # make written duration numerators
        numerators = []
        parts = abjad.mathtools.partition_integer_into_canonic_parts(
            duration.numerator)
        if (forbidden_duration is not None and
            forbidden_duration <= duration):
            for part in parts:
                if forbidden_numerator <= part:
                    better_parts = LeafMaker._partition_less_than_double(
                        part,
                        preferred_numerator,
                        )
                    numerators.extend(better_parts)
                else:
                    numerators.append(part)
        else:
            numerators = parts
        # reverse numerators if necessary
        if not decrease_monotonic:
            numerators = list(reversed(numerators))
        # make one leaf per written duration
        result = []
        for numerator in numerators:
            written_duration = abjad.Duration(
                numerator,
                duration.denominator,
                )
            if pitches is not None:
                arguments = (pitches, written_duration)
            else:
                arguments = (written_duration, )
            result.append(class_(*arguments))
        result = abjad.select(result)
        # apply tie spanner if required
        if tie_parts and 1 < len(result):
            if not issubclass(class_, (abjad.Rest, abjad.Skip)):
                tie = abjad.Tie(repeat=repeat_ties)
                abjad.attach(tie, result)
        # return result
        return result

    @staticmethod
    def _partition_less_than_double(n, m):
        import abjad
        assert abjad.mathtools.is_positive_integer_equivalent_number(n)
        assert abjad.mathtools.is_positive_integer_equivalent_number(m)
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
    def decrease_monotonic(self):
        """
        Is true when durations decrease monotonically.

        Returns true, false or none.
        """
        return self._decrease_monotonic

    @property
    def forbidden_duration(self):
        """
        Gets forbidden written duration.

        Returns duration or none.
        """
        return self._forbidden_duration

    @property
    def metrical_hierarchy(self):
        """
        Gets metrical hierarchy.

        Returns metrical hierarchy or none.
        """
        return self._metrical_hierarchy

    @property
    def skips_instead_of_rests(self):
        """
        Is true when skips appear in place of rests.

        Returns true, false or none.
        """
        return self._skips_instead_of_rests

    @property
    def repeat_ties(self) -> bool:
        """
        Is true when ties are repeat ties.
        """
        return self._repeat_ties

    @property
    def use_multimeasure_rests(self):
        """
        Is true when rests are multimeasure.

        Returns true, false or none.
        """
        return self._use_multimeasure_rests
