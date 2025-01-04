import collections
import fractions
import math
import numbers

from . import _getlib
from . import duration as _duration
from . import exceptions as _exceptions
from . import math as _math
from . import pitch as _pitch
from . import score as _score
from . import sequence as _sequence
from . import spanners as _spanners
from . import tag as _tag
from . import typings as _typings


def _group_by_implied_prolation(durations):
    pairs = []
    for duration in durations:
        if isinstance(duration, tuple):
            pairs.append(duration)
        else:
            pairs.append(duration.pair)
    durations = pairs
    assert 0 < len(durations)
    group = [durations[0]]
    result = [group]
    for d in durations[1:]:
        d_f = set(_math.factors(d[1]))
        d_f.discard(2)
        gd_f = set(_math.factors(group[0][1]))
        gd_f.discard(2)
        if d_f == gd_f:
            group.append(d)
        else:
            group = [d]
            result.append(group)
    return result


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
        _pitch.NamedPitch,
        _pitch.NumberedPitch,
        _pitch.PitchClass,
    )
    chord_prototype = (tuple, list)
    rest_prototype = (type(None),)
    if isinstance(pitch, note_prototype):
        leaves = _make_tied_leaf(
            _score.Note,
            duration,
            increase_monotonic=increase_monotonic,
            forbidden_duration=forbidden_note_duration,
            pitches=pitch,
            tag=tag,
        )
    elif isinstance(pitch, chord_prototype):
        leaves = _make_tied_leaf(
            _score.Chord,
            duration,
            increase_monotonic=increase_monotonic,
            forbidden_duration=forbidden_note_duration,
            pitches=pitch,
            tag=tag,
        )
    elif isinstance(pitch, rest_prototype) and skips_instead_of_rests:
        leaves = _make_tied_leaf(
            _score.Skip,
            duration,
            increase_monotonic=increase_monotonic,
            forbidden_duration=forbidden_rest_duration,
            pitches=None,
            tag=tag,
        )
    elif isinstance(pitch, rest_prototype) and not use_multimeasure_rests:
        leaves = _make_tied_leaf(
            _score.Rest,
            duration,
            increase_monotonic=increase_monotonic,
            forbidden_duration=forbidden_rest_duration,
            pitches=None,
            tag=tag,
        )
    elif isinstance(pitch, rest_prototype) and use_multimeasure_rests:
        multimeasure_rest = _score.MultimeasureRest((1), tag=tag)
        multimeasure_rest.multiplier = duration
        leaves = (multimeasure_rest,)
    else:
        raise ValueError(f"unknown pitch: {pitch!r}.")
    return leaves


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
    duration = _duration.Duration(duration)
    duration_pair = duration.pair
    if forbidden_duration is not None:
        assert forbidden_duration.is_assignable
        assert forbidden_duration.numerator == 1
    # find preferred numerator of written durations if necessary
    if forbidden_duration is not None and forbidden_duration <= fractions.Fraction(
        *duration_pair
    ):
        denominators = [
            2 * forbidden_duration.denominator,
            duration_pair[1],
        ]
        denominator = _math.least_common_multiple(*denominators)
        pair = _duration.with_denominator(forbidden_duration, denominator)
        forbidden_numerator = pair[0]
        assert forbidden_numerator % 2 == 0
        preferred_numerator = forbidden_numerator / 2
        pair = _duration.with_denominator(duration_pair, denominator)
        duration_pair = pair
    # make written duration numerators
    numerators = []
    parts = _math.partition_integer_into_canonic_parts(duration_pair[0])
    if forbidden_duration is not None and fractions.Fraction(
        forbidden_duration
    ) <= fractions.Fraction(*duration_pair):
        for part in parts:
            if forbidden_numerator <= part:
                better_parts = _partition_less_than_double(part, preferred_numerator)
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
        written_duration = _duration.Duration(numerator, duration_pair[1])
        if pitches is not None:
            arguments = (pitches, written_duration)
        else:
            arguments = (written_duration,)
        result.append(class_(*arguments, multiplier=multiplier, tag=tag))
    # tie if required
    if tie_parts and 1 < len(result):
        if not issubclass(class_, (_score.Rest, _score.Skip)):
            _spanners.tie(result)
    return result


def _make_unprolated_notes(pitches, durations, increase_monotonic=None, tag=None):
    assert len(pitches) == len(durations)
    result = []
    for pitch, duration in zip(pitches, durations):
        result.extend(
            _make_tied_leaf(
                _score.Note,
                duration,
                pitches=pitch,
                increase_monotonic=increase_monotonic,
                tag=tag,
            )
        )
    return result


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


def make_leaves(
    pitches,
    durations,
    *,
    forbidden_note_duration: _typings.Duration | None = None,
    forbidden_rest_duration: _typings.Duration | None = None,
    skips_instead_of_rests: bool = False,
    increase_monotonic: bool = False,
    tag: _tag.Tag | None = None,
    use_multimeasure_rests: bool = False,
):
    r"""
    Makes leaves from ``pitches`` and ``durations``.

    ..  container:: example

        Integer and string elements in ``pitches`` result in notes:

        >>> pitches = [2, 4, "F#5", "G#5"]
        >>> duration = abjad.Duration(1, 4)
        >>> leaves = abjad.makers.make_leaves(pitches, duration)
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

        >>> pitches = [(0, 2, 4), ("F#5", "G#5", "A#5")]
        >>> duration = abjad.Duration(1, 2)
        >>> leaves = abjad.makers.make_leaves(pitches, duration)
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

        >>> pitches = 4 * [None]
        >>> durations = [abjad.Duration(1, 4)]
        >>> leaves = abjad.makers.make_leaves(pitches, durations)
        >>> staff = abjad.Staff(leaves, lilypond_type="RhythmicStaff")
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

        >>> pitches = [(0, 2, 4), None, "C#5", "D#5"]
        >>> durations = [abjad.Duration(1, 4)]
        >>> leaves = abjad.makers.make_leaves(pitches, durations)
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

        >>> pitches = "e'' ef'' d'' df'' c''"
        >>> durations = [abjad.Duration(1, 4)]
        >>> leaves = abjad.makers.make_leaves(pitches, durations)
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

        Reads ``pitches`` cyclically when the length of ``pitches`` is less than the
        length of ``durations``:

        >>> pitches = ["C5"]
        >>> durations = 2 * [abjad.Duration(3, 8), abjad.Duration(1, 8)]
        >>> leaves = abjad.makers.make_leaves(pitches, durations)
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

        Reads ``durations`` cyclically when the length of ``durations`` is less than the
        length of ``pitches``:

        >>> pitches = "c'' d'' e'' f''"
        >>> durations = [abjad.Duration(1, 4)]
        >>> leaves = abjad.makers.make_leaves(pitches, durations)
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

        >>> pitches = ["D5"]
        >>> durations = 3 * [abjad.Duration(1, 3)]
        >>> leaves = abjad.makers.make_leaves(pitches, durations)
        >>> staff = abjad.Staff(leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tuplet 3/2
                {
                    d''2
                    d''2
                    d''2
                }
            }

    ..  container:: example

        Set ``increase_monotonic`` to false to return nonassignable durations tied from
        greatest to least:

        >>> pitches = ["D#5"]
        >>> durations = [abjad.Duration(13, 16)]
        >>> leaves = abjad.makers.make_leaves(pitches, durations)
        >>> staff = abjad.Staff(leaves)
        >>> score = abjad.Score([staff], name="Score")
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

        Set ``increase_monotonic`` to true to return nonassignable durations tied from
        least to greatest:

        >>> pitches = ["E5"]
        >>> durations = [abjad.Duration(13, 16)]
        >>> leaves = abjad.makers.make_leaves(pitches, durations, increase_monotonic=True)
        >>> staff = abjad.Staff(leaves)
        >>> score = abjad.Score([staff], name="Score")
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

        Set ``forbidden_note_duration`` to avoid notes greater than or equal to a certain
        written duration:

        >>> pitches = "f' g'"
        >>> durations = [abjad.Duration(5, 8)]
        >>> leaves = abjad.makers.make_leaves(pitches, durations,
        ...     forbidden_note_duration=abjad.Duration(1, 2))
        >>> staff = abjad.Staff(leaves)
        >>> score = abjad.Score([staff], name="Score")
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

        You may set ``forbidden_note_duration`` and ``increase_monotonic`` together:

        >>> pitches = "f' g'"
        >>> durations = [abjad.Duration(5, 8)]
        >>> leaves = abjad.makers.make_leaves(
        ...     pitches, durations,
        ...     forbidden_note_duration=abjad.Duration(1, 2),
        ...     increase_monotonic=True,
        ... )
        >>> staff = abjad.Staff(leaves)
        >>> score = abjad.Score([staff], name="Score")
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

        >>> pitches = "f'"
        >>> durations = [abjad.Duration(5, 14)]
        >>> leaves = abjad.makers.make_leaves(pitches, durations)
        >>> staff = abjad.Staff(leaves)
        >>> score = abjad.Score([staff], name="Score")
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
                \tuplet 14/8
                {
                    #(ly:expect-warning "strange time signature found")
                    \time 5/14
                    f'2
                    ~
                    f'8
                }
            }

        This is default behavior.

    ..  container:: example

        None-valued elements in ``pitches`` result in multimeasure rests when the
        multimeasure rest keyword is set:

        >>> pitches = [None]
        >>> durations = [abjad.Duration(3, 8), abjad.Duration(5, 8)]
        >>> leaves = abjad.makers.make_leaves(pitches, durations,
        ...     use_multimeasure_rests=True)
        >>> leaves
        [MultimeasureRest('R1 * 3/8'), MultimeasureRest('R1 * 5/8')]

        >>> staff = abjad.Staff(leaves, lilypond_type="RhythmicStaff")
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 8)), leaves[0])
        >>> abjad.attach(abjad.TimeSignature((5, 8)), leaves[1])
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

        >>> pitches = [abjad.NumberedPitchClass(6)]
        >>> durations = [abjad.Duration(13, 16)]
        >>> leaves = abjad.makers.make_leaves(pitches, durations)
        >>> staff = abjad.Staff(leaves)
        >>> score = abjad.Score([staff], name="Score")
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

        >>> pitches = [None]
        >>> durations = [abjad.Duration(13, 16)]
        >>> abjad.makers.make_leaves(pitches, durations, skips_instead_of_rests=True)
        [Skip('s2.'), Skip('s16')]

    ..  container:: example

        Integer and string elements in ``pitches`` result in notes:

        >>> tag = abjad.Tag("leaf_maker")
        >>> pitches = [2, 4, "F#5", "G#5"]
        >>> duration = abjad.Duration(1, 4)
        >>> leaves = abjad.makers.make_leaves(pitches, duration, tag=tag)
        >>> staff = abjad.Staff(leaves)
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff, tags=True)
            >>> print(string)
            \new Staff
            {
                %! leaf_maker
                d'4
                %! leaf_maker
                e'4
                %! leaf_maker
                fs''4
                %! leaf_maker
                gs''4
            }

    """
    if isinstance(pitches, str):
        pitches = pitches.split()
    if not isinstance(pitches, collections.abc.Iterable):
        pitches = [pitches]
    if isinstance(durations, numbers.Number | tuple):
        durations = [durations]
    if forbidden_note_duration is not None:
        forbidden_note_duration = _duration.Duration(forbidden_note_duration)
    if forbidden_rest_duration is not None:
        forbidden_rest_duration = _duration.Duration(forbidden_rest_duration)
    nonreduced_fractions = [_duration.Duration(_) for _ in durations]
    size = max(len(nonreduced_fractions), len(pitches))
    nonreduced_fractions = _sequence.repeat_to_length(nonreduced_fractions, size)
    pitches = _sequence.repeat_to_length(pitches, size)
    duration_groups = _group_by_implied_prolation(nonreduced_fractions)
    result: list[_score.Tuplet | _score.Leaf] = []
    for duration_group in duration_groups:
        factors_ = _math.factors(duration_group[0][1])
        factors = set(factors_)
        factors.discard(1)
        factors.discard(2)
        current_pitches = pitches[0 : len(duration_group)]
        pitches = pitches[len(duration_group) :]
        if len(factors) == 0:
            for pitch, duration in zip(current_pitches, duration_group):
                leaves = _make_leaf_on_pitch(
                    pitch,
                    duration,
                    increase_monotonic=increase_monotonic,
                    forbidden_note_duration=forbidden_note_duration,
                    forbidden_rest_duration=forbidden_rest_duration,
                    skips_instead_of_rests=skips_instead_of_rests,
                    tag=tag,
                    use_multimeasure_rests=use_multimeasure_rests,
                )
                result.extend(leaves)
        else:
            denominator = duration_group[0][1]
            numerator = _math.greatest_power_of_two_less_equal(denominator)
            multiplier = (numerator, denominator)
            ratio = 1 / _duration.Duration(*multiplier)
            duration_group = [
                ratio * _duration.Duration(duration) for duration in duration_group
            ]
            tuplet_leaves: list[_score.Leaf] = []
            for pitch, duration in zip(current_pitches, duration_group):
                leaves = _make_leaf_on_pitch(
                    pitch,
                    duration,
                    increase_monotonic=increase_monotonic,
                    skips_instead_of_rests=skips_instead_of_rests,
                    tag=tag,
                    use_multimeasure_rests=use_multimeasure_rests,
                )
                tuplet_leaves.extend(leaves)
            tuplet = _score.Tuplet(multiplier, tuplet_leaves)
            result.append(tuplet)
    return result


def make_notes(
    pitches, durations, *, increase_monotonic: bool = False, tag: _tag.Tag | None = None
) -> list[_score.Note | _score.Tuplet]:
    r"""
    Makes notes from ``pitches`` and ``durations``.

    Set ``pitches`` to a single pitch or a sequence of pitches.

    Set ``durations`` to a single duration or a list of durations.

    ..  container:: example

        Cycles through ``pitches`` when the length of ``pitches`` is less than
        the length of ``durations``:

        >>> pitches = [0]
        >>> durations = [(1, 16), (1, 8), (1, 8)]
        >>> notes = abjad.makers.make_notes(pitches, durations)
        >>> staff = abjad.Staff(notes)
        >>> score = abjad.Score([staff], name="Score")
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

        Cycles through ``durations`` when the length of ``durations`` is less than the
        length of ``pitches``:

        >>> pitches = [0, 2, 4, 5, 7]
        >>> durations = [(1, 16), (1, 8), (1, 8)]
        >>> notes = abjad.makers.make_notes(pitches, durations)
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

        >>> pitches = [0]
        >>> durations = [(1, 16), (1, 12), (1, 8)]
        >>> notes = abjad.makers.make_notes(pitches, durations)
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'16
                \tweak edge-height #'(0.7 . 0)
                \tuplet 3/2
                {
                    c'8
                }
                c'8
            }

    ..  container:: example

        Tied values are written in decreasing duration by default:

        >>> pitches = [0]
        >>> durations = [(13, 16)]
        >>> notes = abjad.makers.make_notes(pitches, durations)
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

        Set ``increase_monotonic=True`` to express tied values in increasing duration:

        >>> pitches = [0]
        >>> durations = [(13, 16)]
        >>> notes = abjad.makers.make_notes(pitches, durations, increase_monotonic=True)
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

        >>> pitches = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
        >>> durations = [(1, 8)]
        >>> notes = abjad.makers.make_notes(pitches, durations)
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

    ..  container:: example

        Tag output like this:

        >>> pitches = [0]
        >>> durations = [(1, 16), (1, 8), (1, 8)]
        >>> tag = abjad.Tag("note_maker")
        >>> notes = abjad.makers.make_notes(pitches, durations, tag=tag)
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff, tags=True)
            >>> print(string)
            \new Staff
            {
                %! note_maker
                c'16
                %! note_maker
                c'8
                %! note_maker
                c'8
            }

    """
    if isinstance(pitches, str):
        pitches = pitches.split()
    if not isinstance(pitches, collections.abc.Iterable):
        pitches = [pitches]
    if isinstance(durations, numbers.Number | tuple):
        durations = [durations]
    pairs = []
    for duration in durations:
        if isinstance(duration, tuple):
            pairs.append(duration)
        elif isinstance(duration, int):
            pair = (duration, 1)
            pairs.append(pair)
        else:
            pairs.append(duration.pair)
    size = max(len(pairs), len(pitches))
    pairs = _sequence.repeat_to_length(pairs, size)
    pitches = _sequence.repeat_to_length(pitches, size)
    durations = _group_by_implied_prolation(pairs)
    result: list[_score.Note | _score.Tuplet] = []
    for duration in durations:
        factors = set(_math.factors(duration[0][1]))
        factors.discard(1)
        factors.discard(2)
        ps = pitches[0 : len(duration)]
        pitches = pitches[len(duration) :]
        if len(factors) == 0:
            result.extend(
                _make_unprolated_notes(
                    ps,
                    duration,
                    increase_monotonic=increase_monotonic,
                    tag=tag,
                )
            )
        else:
            denominator = duration[0][1]
            numerator = _math.greatest_power_of_two_less_equal(denominator)
            multiplier = _duration.Duration(numerator, denominator)
            ratio = multiplier.reciprocal
            duration = [ratio * _duration.Duration(d) for d in duration]
            ns = _make_unprolated_notes(
                ps,
                duration,
                increase_monotonic=increase_monotonic,
                tag=tag,
            )
            tuplet = _score.Tuplet(multiplier.pair, ns)
            result.append(tuplet)
    return result


def tuplet_from_duration_and_ratio(
    duration,
    ratio: tuple[int, ...],
    *,
    increase_monotonic: bool = False,
    tag: _tag.Tag | None = None,
) -> _score.Tuplet:
    r"""
    Makes tuplet from ``duration`` and ``ratio``.

    ..  container:: example

        Makes tupletted leaves strictly without dots when all ``ratio`` equal ``1``:

        >>> tuplet = abjad.makers.tuplet_from_duration_and_ratio(
        ...     abjad.Duration(3, 16),
        ...     (1, 1, 1, -1, -1),
        ... )
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tuplet 5/4
            {
                \time 3/16
                c'32.
                c'32.
                c'32.
                r32.
                r32.
            }

        Allows tupletted leaves to return with dots when some ``ratio`` do not equal
        ``1``:

        >>> tuplet = abjad.makers.tuplet_from_duration_and_ratio(
        ...     abjad.Duration(3, 16),
        ...     (1, -2, -2, 3, 3),
        ... )
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 11/6
            {
                \time 3/16
                c'32
                r16
                r16
                c'16.
                c'16.
            }

        Interprets nonassignable ``ratio`` according to ``increase_monotonic``:

        >>> tuplet = abjad.makers.tuplet_from_duration_and_ratio(
        ...     abjad.Duration(3, 16),
        ...     (5, -1, 5),
        ...     increase_monotonic=True,
        ... )
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tuplet 11/8
            {
                \time 3/16
                c'16...
                r64.
                c'16...
            }

    ..  container:: example

        Makes augmented tuplet from ``duration`` and ``ratio`` and encourages dots:

        >>> tuplet = abjad.makers.tuplet_from_duration_and_ratio(
        ...     abjad.Duration(3, 16),
        ...     (1, 1, 1, -1, -1),
        ... )
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tuplet 5/4
            {
                \time 3/16
                c'32.
                c'32.
                c'32.
                r32.
                r32.
            }

        Interprets nonassignable ``ratio`` according to ``increase_monotonic``:

        >>> tuplet = abjad.makers.tuplet_from_duration_and_ratio(
        ...     abjad.Duration(3, 16),
        ...     (5, -1, 5),
        ...     increase_monotonic=True,
        ... )
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tuplet 11/8
            {
                \time 3/16
                c'16...
                r64.
                c'16...
            }

    ..  container:: example

        Makes diminished tuplet from ``duration`` and nonzero integer ``ratio``.

        Makes tupletted leaves strictly without dots when all ``ratio`` equal ``1``:

        >>> tuplet = abjad.makers.tuplet_from_duration_and_ratio(
        ...     abjad.Duration(3, 16),
        ...     (1, 1, 1, -1, -1),
        ... )
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tuplet 5/4
            {
                \time 3/16
                c'32.
                c'32.
                c'32.
                r32.
                r32.
            }

        Allows tupletted leaves to return with dots when some ``ratio`` do not equal
        ``1``:

        >>> tuplet = abjad.makers.tuplet_from_duration_and_ratio(
        ...     abjad.Duration(3, 16),
        ...     (1, -2, -2, 3, 3),
        ... )
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 11/6
            {
                \time 3/16
                c'32
                r16
                r16
                c'16.
                c'16.
            }

        Interprets nonassignable ``ratio`` according to ``increase_monotonic``:

        >>> tuplet = abjad.makers.tuplet_from_duration_and_ratio(
        ...     abjad.Duration(3, 16),
        ...     (5, -1, 5),
        ...     increase_monotonic=True,
        ... )
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tuplet 11/8
            {
                \time 3/16
                c'16...
                r64.
                c'16...
            }

    ..  container:: example

        Makes diminished tuplet from ``duration`` and ``ratio`` and encourages dots:

        >>> tuplet = abjad.makers.tuplet_from_duration_and_ratio(
        ...     abjad.Duration(3, 16),
        ...     (1, 1, 1, -1, -1),
        ... )
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tuplet 5/4
            {
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
        ...     (5, -1, 5),
        ...     increase_monotonic=True,
        ... )
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tuplet 11/8
            {
                \time 3/16
                c'16...
                r64.
                c'16...
            }

    Reduces ``ratio`` relative to each other.

    Interprets negative ``ratio`` as rests.
    """
    duration = _duration.Duration(duration)
    assert isinstance(ratio, tuple), repr(ratio)
    basic_prolated_duration = duration / _math.weight(ratio)
    basic_written_duration = basic_prolated_duration.equal_or_greater_assignable
    written_durations = [x * basic_written_duration for x in ratio]
    notes: list[_score.Leaf | _score.Tuplet]
    try:
        notes = [
            _score.Note(0, x, tag=tag) if 0 < x else _score.Rest(abs(x), tag=tag)
            for x in written_durations
        ]
    except _exceptions.AssignabilityError:
        denominator = duration.denominator
        note_durations = [_duration.Duration(x, denominator) for x in ratio]
        pitches = [None if note_duration < 0 else 0 for note_duration in note_durations]
        leaf_durations = [abs(note_duration) for note_duration in note_durations]
        notes = make_leaves(
            pitches,
            leaf_durations,
            increase_monotonic=increase_monotonic,
            tag=tag,
        )
    tuplet = _score.Tuplet.from_duration(duration, notes, tag=tag)
    tuplet.normalize_multiplier()
    return tuplet


def tuplet_from_leaf_and_ratio(
    leaf: _score.Leaf, ratio: tuple[int, ...]
) -> _score.Tuplet:
    r"""
    Makes tuplet from ``leaf`` and ``ratio``.

    >>> note = abjad.Note("c'8.")

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(note, (1,))
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 1/1
            {
                \time 3/16
                c'8.
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(note, (1, 2))
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 1/1
            {
                \time 3/16
                c'16
                c'8
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(note, (1, 2, 2))
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tuplet 5/4
            {
                \time 3/16
                c'32.
                c'16.
                c'16.
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(note, (1, 2, 2, 3))
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 4/3
            {
                \time 3/16
                c'32
                c'16
                c'16
                c'16.
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(note, (1, 2, 2, 3, 3))
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 11/6
            {
                \time 3/16
                c'32
                c'16
                c'16
                c'16.
                c'16.
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(note, (1, 2, 2, 3, 3, 4))
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tuplet 5/4
            {
                \time 3/16
                c'64
                c'32
                c'32
                c'32.
                c'32.
                c'16
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(note, (1,))
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 1/1
            {
                \time 3/16
                c'8.
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(note, (1, 2))
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 1/1
            {
                \time 3/16
                c'16
                c'8
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(note, (1, 2, 2))
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tuplet 5/4
            {
                \time 3/16
                c'32.
                c'16.
                c'16.
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(note, (1, 2, 2, 3))
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 4/3
            {
                \time 3/16
                c'32
                c'16
                c'16
                c'16.
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(note, (1, 2, 2, 3, 3))
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 11/6
            {
                \time 3/16
                c'32
                c'16
                c'16
                c'16.
                c'16.
            }

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_leaf_and_ratio(note, (1, 2, 2, 3, 3, 4))
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tuplet 5/4
            {
                \time 3/16
                c'64
                c'32
                c'32
                c'32.
                c'32.
                c'16
            }

    """
    assert isinstance(ratio, tuple), repr(ratio)
    target_duration = leaf.written_duration
    basic_prolated_duration = target_duration / sum(ratio)
    basic_written_duration = basic_prolated_duration.equal_or_greater_assignable
    written_durations = [_ * basic_written_duration for _ in ratio]
    notes: list[_score.Note | _score.Tuplet]
    try:
        notes = [_score.Note(0, x) for x in written_durations]
    except _exceptions.AssignabilityError:
        denominator = target_duration.denominator
        note_durations = [_duration.Duration(_, denominator) for _ in ratio]
        notes = make_notes(0, note_durations)
    contents_duration = _getlib._get_duration(notes)
    multiplier = target_duration / contents_duration
    tuplet = _score.Tuplet(_duration.pair(multiplier), notes)
    tuplet.normalize_multiplier()
    return tuplet


def tuplet_from_ratio_and_pair(
    ratio: tuple,
    fraction: tuple,
    *,
    tag: _tag.Tag | None = None,
) -> _score.Tuplet:
    r"""
    Makes tuplet from nonreduced ``ratio`` and nonreduced ``fraction``.

    ..  container:: example

        >>> tuplet = abjad.makers.tuplet_from_ratio_and_pair((1,), (7, 16))
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((7, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 1/1
            {
                \time 7/16
                c'4..
            }

        >>> tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 2), (7, 16))
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((7, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 6/7
            {
                \time 7/16
                c'8
                c'4
            }

        >>> tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 2, 4), (7, 16))
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((7, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 1/1
            {
                \time 7/16
                c'16
                c'8
                c'4
            }

        >>> tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 2, 4, 1), (7, 16))
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((7, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 8/7
            {
                \time 7/16
                c'16
                c'8
                c'4
                c'16
            }

        >>> tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 2, 4, 1, 2), (7, 16))
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((7, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 10/7
            {
                \time 7/16
                c'16
                c'8
                c'4
                c'16
                c'8
            }

        >>> tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 2, 4, 1, 2, 4), (7, 16))
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((7, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tuplet 2/1
            {
                \time 7/16
                c'16
                c'8
                c'4
                c'16
                c'8
                c'4
            }

        Works with nonassignable rests:

        >>> tuplet = abjad.makers.tuplet_from_ratio_and_pair((11, -5), (5, 16))
        >>> staff = abjad.Staff(
        ...     [tuplet],
        ...     lilypond_type="RhythmicStaff",
        ... )
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((7, 16)), tuplet[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff[0])
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 8/5
            {
                \time 7/16
                c'4
                ~
                c'16.
                r8
                r32
            }

    Interprets ``d`` as tuplet denominator.
    """
    if not isinstance(ratio, tuple):
        raise ValueError(f"must be tuple, not {ratio!r}.")
    if not isinstance(fraction, tuple):
        raise ValueError(f"must be pair, not {fraction!r}.")
    numerator, denominator = fraction
    duration = _duration.Duration(fraction)
    if len(ratio) == 1:
        if 0 < ratio[0]:
            try:
                note = _score.Note(0, duration, tag=tag)
                duration = note._get_duration()
                tuplet = _score.Tuplet.from_duration(duration, [note], tag=tag)
                return tuplet
            except _exceptions.AssignabilityError:
                notes = make_notes(0, duration, tag=tag)
                duration = _getlib._get_duration(notes)
                return _score.Tuplet.from_duration(duration, notes, tag=tag)
        elif ratio[0] < 0:
            try:
                rest = _score.Rest(duration, tag=tag)
                duration = rest._get_duration()
                return _score.Tuplet.from_duration(duration, [rest], tag=tag)
            except _exceptions.AssignabilityError:
                rests = make_leaves([None], duration, tag=tag)
                duration = _getlib._get_duration(rests)
                return _score.Tuplet.from_duration(duration, rests, tag=tag)
        else:
            raise ValueError("no divide zero values.")
    else:
        exponent = int(math.log(_math.weight(ratio), 2) - math.log(numerator, 2))
        denominator = int(denominator * 2**exponent)
        components: list[_score.Leaf | _score.Tuplet] = []
        for x in ratio:
            if not x:
                raise ValueError("no divide zero values.")
            if 0 < x:
                try:
                    note = _score.Note(0, (x, denominator), tag=tag)
                    components.append(note)
                except _exceptions.AssignabilityError:
                    notes = make_notes(0, (x, denominator), tag=tag)
                    components.extend(notes)
            else:
                try:
                    rest = _score.Rest((-x, denominator), tag=tag)
                    components.append(rest)
                except _exceptions.AssignabilityError:
                    rests = make_leaves(None, (-x, denominator), tag=tag)
                    components.extend(rests)
        return _score.Tuplet.from_duration(duration, components, tag=tag)
