"""
Makers.
"""

import math

from . import duration as _duration
from . import get as _get
from . import iterate as _iterate
from . import math as _math
from . import pitch as _pitch
from . import score as _score
from . import sequence as _sequence
from . import spanners as _spanners
from . import tag as _tag
from . import tweaks as _tweaks


def _group_by_prolation(durations):
    assert all(isinstance(_, _duration.Duration) for _ in durations), repr(durations)
    assert 0 < len(durations)
    duration_list = [durations[0]]
    duration_lists = [duration_list]
    for duration in durations[1:]:
        duration_denominator_factors = set(_math.factors(duration.denominator))
        duration_denominator_factors.discard(2)
        group_zero_denominator_factors = set(
            _math.factors(duration_list[0].denominator)
        )
        group_zero_denominator_factors.discard(2)
        if duration_denominator_factors == group_zero_denominator_factors:
            duration_list.append(duration)
        else:
            duration_list = [duration]
            duration_lists.append(duration_list)
    return duration_lists


def _make_leaf_on_pitch(
    pitch_list,
    duration,
    *,
    increase_monotonic=False,
    forbidden_note_duration=None,
    forbidden_rest_duration=None,
    skips_instead_of_rests=False,
    tag=None,
    use_multimeasure_rests=False,
):
    assert isinstance(pitch_list, list), repr(pitch_list)
    assert all(isinstance(_, _pitch.NamedPitch) for _ in pitch_list), repr(pitch_list)
    assert isinstance(duration, _duration.Duration), repr(duration)
    if pitch_list == []:
        if skips_instead_of_rests is True:
            leaves = _make_tied_leaf(
                _score.Skip,
                duration,
                increase_monotonic=increase_monotonic,
                forbidden_duration=forbidden_rest_duration,
                pitches=None,
                tag=tag,
            )
        elif use_multimeasure_rests is True:
            multimeasure_rest = _score.MultimeasureRest((1), tag=tag)
            multimeasure_rest.set_multiplier(duration.pair())
            leaves = [multimeasure_rest]
        else:
            leaves = _make_tied_leaf(
                _score.Rest,
                duration,
                increase_monotonic=increase_monotonic,
                forbidden_duration=forbidden_rest_duration,
                pitches=None,
                tag=tag,
            )
    elif len(pitch_list) == 1:
        pitch = pitch_list[0]
        leaves = _make_tied_leaf(
            _score.Note,
            duration,
            increase_monotonic=increase_monotonic,
            forbidden_duration=forbidden_note_duration,
            pitches=pitch,
            tag=tag,
        )
    else:
        leaves = _make_tied_leaf(
            _score.Chord,
            duration,
            increase_monotonic=increase_monotonic,
            forbidden_duration=forbidden_note_duration,
            pitches=pitch_list,
            tag=tag,
        )
    assert isinstance(leaves, list), repr(leaves)
    assert all(isinstance(_, _score.Leaf) for _ in leaves), repr(leaves)
    return leaves


def _make_tied_leaf(
    class_,
    duration,
    increase_monotonic=False,
    forbidden_duration=None,
    multiplier=None,
    pitches=None,
    tag=None,
):
    assert isinstance(duration, _duration.Duration), repr(duration)
    if multiplier is not None:
        assert isinstance(multiplier, tuple), repr(multiplier)
    duration_pair = duration.pair()
    if forbidden_duration is not None:
        assert forbidden_duration.is_assignable()
        assert forbidden_duration.numerator == 1
    if forbidden_duration is not None and forbidden_duration <= duration:
        denominators = [2 * forbidden_duration.denominator, duration.denominator]
        denominator = _math.least_common_multiple(*denominators)
        forbidden_pair = _duration.with_denominator(forbidden_duration, denominator)
        forbidden_numerator = forbidden_pair[0]
        assert forbidden_numerator % 2 == 0
        preferred_numerator = forbidden_numerator / 2
        duration_pair = _duration.with_denominator(duration_pair, denominator)
    parts = _math.partition_integer_into_canonic_parts(duration_pair[0])
    if forbidden_duration is not None and forbidden_duration <= duration:
        numerators = []
        for part in parts:
            if forbidden_numerator <= part:
                better_parts = _partition_less_than_double(part, preferred_numerator)
                numerators.extend(better_parts)
            else:
                numerators.append(part)
    else:
        numerators = parts
    if increase_monotonic:
        numerators = list(reversed(numerators))
    leaves = []
    for numerator in numerators:
        written_duration = _duration.Duration(numerator, duration_pair[1])
        if pitches is not None:
            arguments = (pitches, written_duration)
        else:
            arguments = (written_duration,)
        leaf = class_(*arguments, multiplier=multiplier, tag=tag)
        leaves.append(leaf)
    if 1 < len(leaves):
        if not issubclass(class_, _score.Rest | _score.Skip):
            _spanners.tie(leaves)
    assert isinstance(leaves, list), repr(leaves)
    assert all(isinstance(_, _score.Leaf) for _ in leaves), repr(leaves)
    return leaves


def _make_unprolated_notes(pitches, durations, *, increase_monotonic=None, tag=None):
    assert all(isinstance(_, _duration.Duration) for _ in durations), repr(durations)
    notes = []
    for pitch, duration in zip(pitches, durations, strict=True):
        notes_ = _make_tied_leaf(
            _score.Note,
            duration,
            pitches=pitch,
            increase_monotonic=increase_monotonic,
            tag=tag,
        )
        notes.extend(notes_)
    assert all(isinstance(_, _score.Note) for _ in notes), repr(notes)
    return notes


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


def make_durations(items: list) -> list[_duration.Duration]:
    """
    Changes list of arbitrary ``items`` to list of durations.

    ..  container:: example

        >>> abjad.makers.make_durations([(1, 8), (1, 2), (1, 16)])
        [Duration(1, 8), Duration(1, 2), Duration(1, 16)]

    """
    durations = [_duration.Duration(_) for _ in items]
    return durations


def make_leaves(
    pitch_lists: list[list[_pitch.NamedPitch]],
    durations: list[_duration.Duration],
    *,
    forbidden_note_duration: _duration.Duration | None = None,
    forbidden_rest_duration: _duration.Duration | None = None,
    increase_monotonic: bool = False,
    skips_instead_of_rests: bool = False,
    tag: _tag.Tag | None = None,
    use_multimeasure_rests: bool = False,
):
    r"""
    Makes leaves from ``pitch_lists`` and ``durations``.

    ..  container:: example

        Interprets empty pitch lists as rests:

        >>> items = [[], [], [], []]
        >>> pitch_lists = abjad.makers.make_pitch_lists(items)
        >>> leaves = abjad.makers.make_leaves(pitch_lists, [abjad.Duration(1, 4)])
        >>> staff = abjad.Staff(leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                r4
                r4
                r4
                r4
            }

        Interprets length-1 pitch lists as notes:

        >>> items = [2, 4, "F#5", "G#5"]
        >>> pitch_lists = abjad.makers.make_pitch_lists(items)
        >>> leaves = abjad.makers.make_leaves(pitch_lists, [abjad.Duration(1, 4)])
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

        Interprets pitch lists with length greater than 1 as chords:

        >>> items = [[0, 2, 4], ["F#5", "G#5", "A#5"]]
        >>> pitch_lists = abjad.makers.make_pitch_lists(items)
        >>> leaves = abjad.makers.make_leaves(pitch_lists, [abjad.Duration(1, 4)])
        >>> staff = abjad.Staff(leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <c' d' e'>4
                <fs'' gs'' as''>4
            }

        Interprets mixed types of pitch list like this:

        >>> items = [[0, 2, 4], [], "C#5", "D#5"]
        >>> pitch_lists = abjad.makers.make_pitch_lists(items)
        >>> leaves = abjad.makers.make_leaves(pitch_lists, [abjad.Duration(1, 4)])
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

        Interprets nondyadic durations as (possibly incomplete) tuplets:

        >>> pitch_list = [abjad.NamedPitch("d''")]
        >>> durations = [abjad.Duration(1, 3)]
        >>> leaves = abjad.makers.make_leaves([pitch_list], durations)
        >>> abjad.makers.tweak_tuplet_bracket_edge_height(leaves)
        >>> staff = abjad.Staff(leaves)
        >>> score = abjad.Score([staff])
        >>> abjad.override(score).TupletBracket.bracket_visibility = True
        >>> abjad.setting(score).tupletFullLength = True
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                \override TupletBracket.bracket-visibility = ##t
                tupletFullLength = ##t
            }
            <<
                \new Staff
                {
                    \tweak edge-height #'(0.7 . 0)
                    \tuplet 3/2
                    {
                        d''2
                    }
                }
            >>

        >>> pitch_list = [abjad.NamedPitch("d''")]
        >>> durations = 2 * [abjad.Duration(1, 3)]
        >>> leaves = abjad.makers.make_leaves([pitch_list], durations)
        >>> abjad.makers.tweak_tuplet_bracket_edge_height(leaves)
        >>> staff = abjad.Staff(leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tweak edge-height #'(0.7 . 0)
                \tuplet 3/2
                {
                    d''2
                    d''2
                }
            }

        >>> pitch_list = [abjad.NamedPitch("d''")]
        >>> durations = 3 * [abjad.Duration(1, 3)]
        >>> leaves = abjad.makers.make_leaves([pitch_list], durations)
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

        >>> pitch_list = [abjad.NamedPitch("d''")]
        >>> leaves = abjad.makers.make_leaves([pitch_list], [abjad.Duration(5, 14)])
        >>> abjad.makers.tweak_tuplet_bracket_edge_height(leaves)
        >>> staff = abjad.Staff(leaves)
        >>> time_signature = abjad.TimeSignature((5, 14))
        >>> leaf = abjad.get.leaf(staff, 0)
        >>> abjad.attach(time_signature, leaf)
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \new Staff
                {
                    \tweak edge-height #'(0.7 . 0)
                    \tuplet 14/8
                    {
                        #(ly:expect-warning "strange time signature found")
                        \time 5/14
                        d''2
                        ~
                        d''8
                    }
                }
            >>

    ..  container:: example

        Reads ``pitch_lists`` cyclically when the length of ``pitch_lists`` is less
        than the length of ``durations``:

        >>> pitch_lists = abjad.makers.make_pitch_lists([[12, 14], []])
        >>> pairs = [(1, 16), (1, 16), (1, 8), (1, 8), (1, 8)]
        >>> durations = abjad.makers.make_durations(pairs)
        >>> leaves = abjad.makers.make_leaves(pitch_lists, durations)
        >>> staff = abjad.Staff(leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <c'' d''>16
                r16
                <c'' d''>8
                r8
                <c'' d''>8
            }

        Reads ``durations`` cyclically when the length of ``durations`` is less
        than the length of ``pitch_lists``:

        >>> pitch_lists = abjad.makers.make_pitch_lists([[12, 14], [], 10, 9, 7])
        >>> durations = [abjad.Duration(1, 16), abjad.Duration(1, 8)]
        >>> leaves = abjad.makers.make_leaves(pitch_lists, durations)
        >>> staff = abjad.Staff(leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <c'' d''>16
                r8
                bf'16
                a'8
                g'16
            }

    ..  container:: example

        Avoids durations greater than or equal to ``forbidden_note_duration``:

        >>> pitch_lists = abjad.makers.make_pitch_lists("f' g'")
        >>> durations = [abjad.Duration(5, 8)]
        >>> leaves = abjad.makers.make_leaves(pitch_lists, durations)
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
                f'2
                ~
                f'8
                g'2
                ~
                g'8
            }

        >>> leaves = abjad.makers.make_leaves(
        ...     pitch_lists,
        ...     durations,
        ...     forbidden_note_duration=abjad.Duration(1, 2),
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

        Writes tied durations in monotonically decreasing order by default:

        >>> pitch_list = [abjad.NamedPitch("ds''")]
        >>> durations = [abjad.Duration(13, 16)]
        >>> leaves = abjad.makers.make_leaves([pitch_list], durations)
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

        Writes tied durations in monotonically increasing order when
        ``increase_monotonic`` is true:

        >>> leaves = abjad.makers.make_leaves(
        ...     [[abjad.NamedPitch("e''")]],
        ...     [abjad.Duration(13, 16)],
        ...     increase_monotonic=True,
        ... )
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

        Interprets empty pitch lists as skips when ``skips_instead_of_rests``
        is true:

        >>> durations = [abjad.Duration(13, 16)]
        >>> abjad.makers.make_leaves([[]], durations, skips_instead_of_rests=True)
        [Skip('s2.'), Skip('s16')]

    ..  container:: example

        Interprets empty pitch lists as multimeasure rests when
        ``use_multimeasure_rests`` is true:

        >>> durations = [abjad.Duration(3, 8), abjad.Duration(5, 8)]
        >>> leaves = abjad.makers.make_leaves(
        ...     [[]],
        ...     durations,
        ...     use_multimeasure_rests=True,
        ... )
        >>> staff = abjad.Staff(leaves)
        >>> abjad.attach(abjad.TimeSignature((3, 8)), leaves[0])
        >>> abjad.attach(abjad.TimeSignature((5, 8)), leaves[1])
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \new Staff
                {
                    \time 3/8
                    R1 * 3/8
                    \time 5/8
                    R1 * 5/8
                }
            >>

    """
    assert isinstance(pitch_lists, list), repr(pitch_lists)
    for pitch_list in pitch_lists:
        assert isinstance(pitch_list, list), repr(pitch_lists)
        assert all(isinstance(_, _pitch.NamedPitch) for _ in pitch_list), repr(
            pitch_lists
        )
    assert all(isinstance(_, _duration.Duration) for _ in durations), repr(durations)
    if forbidden_note_duration is not None:
        assert isinstance(forbidden_note_duration, _duration.Duration)
    if forbidden_rest_duration is not None:
        assert isinstance(forbidden_rest_duration, _duration.Duration)
    maximum_length = max(len(durations), len(pitch_lists))
    durations = _sequence.repeat_to_length(durations, maximum_length)
    pitch_lists = _sequence.repeat_to_length(pitch_lists, maximum_length)
    duration_lists = _group_by_prolation(durations)
    result: list[_score.Tuplet | _score.Leaf] = []
    for duration_list in duration_lists:
        factors_ = _math.factors(duration_list[0].denominator)
        factors = set(factors_)
        factors.discard(1)
        factors.discard(2)
        current_pitch_lists = pitch_lists[0 : len(duration_list)]
        pitch_lists = pitch_lists[len(duration_list) :]
        if len(factors) == 0:
            for pitch_list, duration in zip(current_pitch_lists, duration_list):
                leaves = _make_leaf_on_pitch(
                    pitch_list,
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
            denominator = duration_list[0].denominator
            numerator = _math.greatest_power_of_two_less_equal(denominator)
            multiplier = (numerator, denominator)
            # TODO: do not reduce
            ratio = 1 / _duration.Duration(*multiplier)
            duration_list = [ratio * _ for _ in duration_list]
            tuplet_leaves: list[_score.Leaf] = []
            for pitch_list, duration in zip(current_pitch_lists, duration_list):
                leaves = _make_leaf_on_pitch(
                    pitch_list,
                    duration,
                    increase_monotonic=increase_monotonic,
                    skips_instead_of_rests=skips_instead_of_rests,
                    tag=tag,
                    use_multimeasure_rests=use_multimeasure_rests,
                )
                tuplet_leaves.extend(leaves)
            ratio_ = _duration.Ratio(denominator, numerator)
            tuplet = _score.Tuplet(ratio_, tuplet_leaves)
            result.append(tuplet)
    return result


def make_notes(
    pitches: list[_pitch.NamedPitch],
    durations: list[_duration.Duration],
    *,
    increase_monotonic: bool = False,
    tag: _tag.Tag | None = None,
) -> list[_score.Note | _score.Tuplet]:
    r"""
    Makes notes from ``pitches`` and ``durations``.

    ..  container:: example

        Cycles through ``pitches`` when the length of ``pitches`` is less than
        the length of ``durations``:

        >>> pitches = abjad.makers.make_pitches("c' d'")
        >>> pairs = [(1, 16), (1, 16), (1, 8), (1, 8), (1, 8)]
        >>> durations = abjad.makers.make_durations(pairs)
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
                d'16
                c'8
                d'8
                c'8
            }

        Cycles through ``durations`` when the length of ``durations`` is less
        than the length of ``pitches``:

        >>> pitches = abjad.makers.make_pitches("c' d' e' f' g'")
        >>> durations = abjad.makers.make_durations([(1, 16), (1, 8)])
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
                e'16
                f'8
                g'16
            }

    ..  container:: example

        Interprets nondyadic durations as (possibly incomplete) tuplets:

        >>> pitches = abjad.makers.make_pitches([0])
        >>> durations = abjad.makers.make_durations([(1, 16), (1, 12), (1, 8)])
        >>> components = abjad.makers.make_notes(pitches, durations)
        >>> abjad.makers.tweak_tuplet_bracket_edge_height(components)
        >>> staff = abjad.Staff(components)
        >>> score = abjad.Score([staff])
        >>> abjad.override(score).TupletBracket.bracket_visibility = True
        >>> abjad.setting(score).proportionalNotationDuration = "#1/24"
        >>> abjad.setting(score).tupletFullLength = True
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                \override TupletBracket.bracket-visibility = ##t
                proportionalNotationDuration = #1/24
                tupletFullLength = ##t
            }
            <<
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
            >>

    ..  container:: example

        Writes tied durations in monotonically decreasing order by default:

        >>> pitches = abjad.makers.make_pitches([0])
        >>> durations = [abjad.Duration(13, 16)]
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

        Writes tied durations in monotonically increasing order when
        ``increase_monotonic`` is true:

        >>> pitches = abjad.makers.make_pitches([0])
        >>> durations = [abjad.Duration(13, 16)]
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

    """
    assert isinstance(pitches, list), repr(pitches)
    prototype = _pitch.NamedPitch | _pitch.NumberedPitch
    assert all(isinstance(_, prototype) for _ in pitches), repr(pitches)
    assert all(isinstance(_, _duration.Duration) for _ in durations), repr(durations)
    maximum_length = max(len(pitches), len(durations))
    pitches = _sequence.repeat_to_length(pitches, maximum_length)
    durations = _sequence.repeat_to_length(durations, maximum_length)
    duration_lists = _group_by_prolation(durations)
    result: list[_score.Note | _score.Tuplet] = []
    for duration_list in duration_lists:
        factors = set(_math.factors(duration_list[0].denominator))
        factors.discard(1)
        factors.discard(2)
        pitches_ = pitches[0 : len(duration_list)]
        pitches = pitches[len(duration_list) :]
        if len(factors) == 0:
            notes = _make_unprolated_notes(
                pitches_,
                duration_list,
                increase_monotonic=increase_monotonic,
                tag=tag,
            )
            result.extend(notes)
        else:
            denominator = duration_list[0].denominator
            numerator = _math.greatest_power_of_two_less_equal(denominator)
            duration = _duration.Duration(numerator, denominator)
            duration_list = [duration.reciprocal() * _ for _ in duration_list]
            notes = _make_unprolated_notes(
                pitches_,
                duration_list,
                increase_monotonic=increase_monotonic,
                tag=tag,
            )
            ratio_string = f"{duration.denominator}:{duration.numerator}"
            tuplet = _score.Tuplet(ratio_string, notes)
            result.append(tuplet)
    assert isinstance(result, list), repr(list)
    assert all(isinstance(_, _score.Note | _score.Tuplet) for _ in result), repr(result)
    return result


def make_pitch_lists(argument: list | str) -> list[list[_pitch.NamedPitch]]:
    """
    Changes list or string ``argument`` to list of pitch lists.

    Use this function to format input for ``abjad.makers.make_leaves()``.

    ..  container:: example

        >>> abjad.makers.make_pitch_lists([3, None, [4, 5]])
        [[NamedPitch("ef'")], [], [NamedPitch("e'"), NamedPitch("f'")]]

        >>> abjad.makers.make_pitch_lists([3, [], [4, 5]])
        [[NamedPitch("ef'")], [], [NamedPitch("e'"), NamedPitch("f'")]]

        >>> abjad.makers.make_pitch_lists("e'' ef'' d''")
        [[NamedPitch("e''")], [NamedPitch("ef''")], [NamedPitch("d''")]]

    """
    pitch_lists = []
    if isinstance(argument, str):
        argument = argument.split()
    for item in argument:
        if isinstance(item, list | tuple):
            pitch_list = [_pitch.NamedPitch(_) for _ in item]
        elif item is None:
            pitch_list = []
        else:
            pitch_list = [_pitch.NamedPitch(item)]
        pitch_lists.append(pitch_list)
    return pitch_lists


def make_pitches(argument: list | str) -> list[_pitch.NamedPitch]:
    """
    Changes list or string ``argument`` to list of named pitches.

    Use this function to format input for ``abjad.makers.make_notes()``.

    ..  container:: example

        >>> abjad.makers.make_pitches([3, 16, 16.5])
        [NamedPitch("ef'"), NamedPitch("e''"), NamedPitch("eqs''")]

        >>> abjad.makers.make_pitches("ef' e'' eqs''")
        [NamedPitch("ef'"), NamedPitch("e''"), NamedPitch("eqs''")]

        >>> abjad.makers.make_pitches(["ef'", "e''", "eqs''"])
        [NamedPitch("ef'"), NamedPitch("e''"), NamedPitch("eqs''")]

        >>> abjad.makers.make_pitches([3, "e''", abjad.NamedPitch("eqs''")])
        [NamedPitch("ef'"), NamedPitch("e''"), NamedPitch("eqs''")]

    """
    if isinstance(argument, str):
        argument = argument.split()
    assert not any(_ is None for _ in argument), repr(argument)
    pitches = [_pitch.NamedPitch(_) for _ in argument]
    return pitches


def make_tuplet(
    duration: _duration.Duration,
    proportion: tuple[int, ...],
    *,
    tag: _tag.Tag | None = None,
) -> _score.Tuplet:
    r"""
    Makes tuplet from ``duration`` and ``proportion``.

    ..  container:: example

        Helper function:

        >>> def make_score(tuplet):
        ...     abjad.tweak(tuplet, r"\tweak bracket-visibility ##t")
        ...     abjad.tweak(tuplet, r"\tweak padding #1.5")
        ...     abjad.tweak(tuplet, r"\tweak text #tuplet-number::calc-fraction-text")
        ...     staff = abjad.Staff([tuplet], lilypond_type="RhythmicStaff")
        ...     score = abjad.Score([staff], name="Score")
        ...     duration = abjad.get.duration(tuplet)
        ...     pair = duration.numerator, duration.denominator
        ...     time_signature = abjad.TimeSignature(pair)
        ...     leaf = abjad.select.leaf(staff, 0)
        ...     abjad.attach(time_signature, leaf)
        ...     return score

    ..  container:: example

        Divides duration of 3/16 into increasing number of parts:

        >>> duration, proportion = abjad.Duration(3, 16), (1, 2, 2)
        >>> tuplet = abjad.makers.make_tuplet(duration, proportion)
        >>> score = make_score(tuplet)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> tuplet = score[0][0]
            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak bracket-visibility ##t
            \tweak padding #1.5
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 5/3
            {
                \time 3/16
                c'16
                c'8
                c'8
            }

        >>> duration, proportion = abjad.Duration(3, 16), (1, 2, 2, 3)
        >>> tuplet = abjad.makers.make_tuplet(duration, proportion)
        >>> score = make_score(tuplet)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> tuplet = score[0][0]
            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak bracket-visibility ##t
            \tweak padding #1.5
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 4/3
            {
                \time 3/16
                c'32
                c'16
                c'16
                c'16.
            }

        >>> duration, proportion = abjad.Duration(3, 16), (1, 2, 2, 3, 3)
        >>> tuplet = abjad.makers.make_tuplet(duration, proportion)
        >>> score = make_score(tuplet)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> tuplet = score[0][0]
            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak bracket-visibility ##t
            \tweak padding #1.5
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

        Divides duration of 7/16 into increasing number of parts:

        >>> duration, proportion = abjad.Duration(7, 16), (1, 2, 2)
        >>> tuplet = abjad.makers.make_tuplet(duration, proportion)
        >>> score = make_score(tuplet)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> tuplet = score[0][0]
            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak bracket-visibility ##t
            \tweak padding #1.5
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 10/7
            {
                \time 7/16
                c'8
                c'4
                c'4
            }

        >>> duration, proportion = abjad.Duration(7, 16), (1, 2, 2, 3)
        >>> tuplet = abjad.makers.make_tuplet(duration, proportion)
        >>> score = make_score(tuplet)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> tuplet = score[0][0]
            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak bracket-visibility ##t
            \tweak padding #1.5
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 8/7
            {
                \time 7/16
                c'16
                c'8
                c'8
                c'8.
            }

        >>> duration, proportion = abjad.Duration(7, 16), (1, 2, 2, 3, 3)
        >>> tuplet = abjad.makers.make_tuplet(duration, proportion)
        >>> score = make_score(tuplet)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> tuplet = score[0][0]
            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak bracket-visibility ##t
            \tweak padding #1.5
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 11/7
            {
                \time 7/16
                c'16
                c'8
                c'8
                c'8.
                c'8.
            }

    ..  container:: example

        Interprets negative integers in ``proportion`` as rests:

        >>> duration, proportion = abjad.Duration(1, 4), (1, 1, 1, -1, 1)
        >>> tuplet = abjad.makers.make_tuplet(duration, proportion)
        >>> score = make_score(tuplet)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> tuplet = score[0][0]
            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak bracket-visibility ##t
            \tweak padding #1.5
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 5/4
            {
                \time 1/4
                c'16
                c'16
                c'16
                r16
                c'16
            }

        >>> duration, proportion = abjad.Duration(1, 4), (3, -2, 2)
        >>> tuplet = abjad.makers.make_tuplet(duration, proportion)
        >>> score = make_score(tuplet)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> tuplet = score[0][0]
            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak bracket-visibility ##t
            \tweak padding #1.5
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 7/4
            {
                \time 1/4
                c'8.
                r8
                c'8
            }

    ..  container:: example

        Works with nonassignable rests:

        >>> duration, proportion = abjad.Duration(7, 16), (11, -5)
        >>> tuplet = abjad.makers.make_tuplet(duration, proportion)
        >>> score = make_score(tuplet)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> tuplet = score[0][0]
            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak bracket-visibility ##t
            \tweak padding #1.5
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 8/7
            {
                \time 7/16
                c'4
                ~
                c'16.
                r8
                r32
            }

    ..  container:: example

        Reduces integers in ``proportion`` relative to each other:

        >>> duration, proportion = abjad.Duration(1, 4), (1, 1, 1)
        >>> tuplet = abjad.makers.make_tuplet(duration, proportion)
        >>> score = make_score(tuplet)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> tuplet = score[0][0]
            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak bracket-visibility ##t
            \tweak padding #1.5
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 3/2
            {
                \time 1/4
                c'8
                c'8
                c'8
            }

        >>> duration, proportion = abjad.Duration(1, 4), (4, 4, 4)
        >>> tuplet = abjad.makers.make_tuplet(duration, proportion)
        >>> score = make_score(tuplet)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> tuplet = score[0][0]
            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak bracket-visibility ##t
            \tweak padding #1.5
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 3/2
            {
                \time 1/4
                c'8
                c'8
                c'8
            }

    """
    assert isinstance(duration, _duration.Duration), repr(duration)
    assert isinstance(proportion, tuple), repr(proportion)
    assert all(isinstance(_, int) for _ in proportion), repr(proportion)
    assert not any(_ == 0 for _ in proportion), repr(proportion)
    if len(proportion) == 1:
        if 0 < proportion[0]:
            pitch_list = [_pitch.NamedPitch("c'")]
        else:
            assert proportion[0] < 0, repr(proportion)
            pitch_list = []
        leaves = make_leaves([pitch_list], [duration], tag=tag)
        tuplet = _score.Tuplet("1:1", leaves, tag=tag)
    else:
        numerator, denominator = duration.pair()
        exponent = int(math.log(_math.weight(proportion), 2) - math.log(numerator, 2))
        denominator = int(denominator * 2**exponent)
        components: list[_score.Leaf | _score.Tuplet] = []
        for item in proportion:
            if 0 < item:
                pitch_list = [_pitch.NamedPitch("c'")]
            else:
                assert item < 0, repr(item)
                pitch_list = []
            duration_ = _duration.Duration(abs(item), denominator)
            leaves = make_leaves([pitch_list], [duration_], tag=tag)
            components.extend(leaves)
        multiplier = duration / _get.duration(components)
        ratio = _duration.Ratio(multiplier.denominator, multiplier.numerator)
        tuplet = _score.Tuplet(ratio, components, tag=tag)
    tuplet.normalize_ratio()
    if tuplet.ratio().is_augmented():
        tuplet.toggle_prolation()
    assert tuplet.ratio().is_canonical() or str(tuplet.ratio()) == "1:1", repr(
        tuplet.ratio()
    )
    return tuplet


def tweak_tuplet_bracket_edge_height(argument) -> None:
    r"""
    Tweaks tuplet bracket edge height of incomplete tuplets in ``argument``.

    A tuplet is defined as incomplete when the denominator ``d`` of the
    tuplet's duration ``n/d`` is nondyadic. For example, the duration of
    ``\tuplet 3/2 { c'4 d'4 }`` is nondyadic because the denominator of ``2/3 *
    2/4 = 1/3`` is 3. But the duration of ``\tuplet 3/2 { c'4 d'4 e'4 }`` is
    dyadic because the denominator of ``2/3 * 3/4 = 1/2`` is 2.

    ..  container:: example

        By default, LilyPond engraves all tuplets with a complete bracket,
        even those that are incomplete, like the first tuplet below:

        >>> string = r"\tuplet 3/2 { c'4 d'4 } \tuplet 3/2 { c'4 d'4 e'4 }"
        >>> staff = abjad.Staff(string)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tuplet 3/2
                {
                    c'4
                    d'4
                }
                \tuplet 3/2
                {
                    c'4
                    d'4
                    e'4
                }
            }

        Call ``abjad.makers.tweak_tuplet_bracket_edge_height()`` to adjust
        the right edge of incomplete tuplets:

        >>> abjad.makers.tweak_tuplet_bracket_edge_height(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tweak edge-height #'(0.7 . 0)
                \tuplet 3/2
                {
                    c'4
                    d'4
                }
                \tuplet 3/2
                {
                    c'4
                    d'4
                    e'4
                }
            }

    """
    for tuplet in _iterate.components(argument, _score.Tuplet):
        duration = tuplet._get_preprolated_duration()
        denominator = duration.denominator
        if not _math.is_nonnegative_integer_power_of_two(denominator):
            _tweaks.tweak(tuplet, r"\tweak edge-height #'(0.7 . 0)")
