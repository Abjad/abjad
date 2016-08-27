# -*- coding: utf-8 -*-
import numbers
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools.topleveltools import attach


def make_leaves(
    pitches,
    durations,
    decrease_durations_monotonically=True,
    forbidden_written_duration=None,
    is_diminution=True,
    metrical_hiearchy=None,
    use_messiaen_style_ties=False,
    use_multimeasure_rests=False,
    ):
    r'''Makes leaves.

    ..  container:: example

        **Example 1.** Integer and string elements in `pitches` result in
        notes:

        ::

            >>> pitches = [2, 4, 'F#5', 'G#5']
            >>> duration = Duration(1, 4)
            >>> leaves = scoretools.make_leaves(pitches, duration)
            >>> staff = Staff(leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                d'4
                e'4
                fs''4
                gs''4
            }

    ..  container:: example

        **Example 2.** Tuple elements in `pitches` result in chords:

        ::

            >>> pitches = [(0, 2, 4), ('F#5', 'G#5', 'A#5')]
            >>> duration = Duration(1, 2)
            >>> leaves = scoretools.make_leaves(pitches, duration)
            >>> staff = Staff(leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                <c' d' e'>2
                <fs'' gs'' as''>2
            }

    ..  container:: example

        **Example 3.** None-valued elements in `pitches` result in rests:

        ::

            >>> pitches = 4 * [None]
            >>> durations = [Duration(1, 4)]
            >>> leaves = scoretools.make_leaves(pitches, durations)
            >>> staff = Staff(leaves)
            >>> staff.context_name = 'RhythmicStaff'
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new RhythmicStaff {
                r4
                r4
                r4
                r4
            }

    ..  container:: example

        **Example 4.** You can mix and match values passed to `pitches`:

        ::

            >>> pitches = [(0, 2, 4), None, 'C#5', 'D#5']
            >>> durations = [Duration(1, 4)]
            >>> leaves = scoretools.make_leaves(pitches, durations)
            >>> staff = Staff(leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                <c' d' e'>4
                r4
                cs''4
                ds''4
            }

    ..  container:: example

        **Example 5.** Read `pitches` cyclically when the length of `pitches`
        is less than the length of `durations`:

        ::

            >>> pitches = ['C5']
            >>> durations = 2 * [Duration(3, 8), Duration(1, 8)]
            >>> leaves = scoretools.make_leaves(pitches, durations)
            >>> staff = Staff(leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c''4.
                c''8
                c''4.
                c''8
            }

    ..  container:: example

        **Example 6.** Read `durations` cyclically when the length of
        `durations` is less than the length of `pitches`:

        ::

            >>> pitches = "c'' d'' e'' f''"
            >>> durations = [Duration(1, 4)]
            >>> leaves = scoretools.make_leaves(pitches, durations)
            >>> staff = Staff(leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c''4
                d''4
                e''4
                f''4
            }

    ..  container:: example

        **Example 7.** Elements in `durations` with non-power-of-two
        denominators result in tuplet-nested leaves:

        ::

            >>> pitches = ['D5']
            >>> durations = [Duration(1, 3), Duration(1, 3), Duration(1, 3)]
            >>> leaves = scoretools.make_leaves(pitches, durations)
            >>> staff = Staff(leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \times 2/3 {
                    d''2
                    d''2
                    d''2
                }
            }

    ..  container:: example

        **Example 8.** Set `decrease_durations_monotonically` to true to
        return nonassignable durations tied from greatest to least:

        ::

            >>> pitches = ['D#5']
            >>> durations = [Duration(13, 16)]
            >>> leaves = scoretools.make_leaves(pitches, durations)
            >>> staff = Staff(leaves)
            >>> time_signature = TimeSignature((13, 16))
            >>> attach(time_signature, staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \time 13/16
                ds''2. ~
                ds''16
            }

    ..  container:: example

        **Example 9.** Set `decrease_durations_monotonically` to false
        to return nonassignable durations tied from least to greatest:

        ::

            >>> pitches = ['E5']
            >>> durations = [Duration(13, 16)]
            >>> leaves = scoretools.make_leaves(
            ...     pitches,
            ...     durations,
            ...     decrease_durations_monotonically=False,
            ...     )
            >>> staff = Staff(leaves)
            >>> time_signature = TimeSignature((13, 16))
            >>> attach(time_signature, staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \time 13/16
                e''16 ~
                e''2.
            }

    ..  container:: example

        **Example 10.** Set `forbidden_written_duration` to avoid notes
        greater than or equal to a certain written duration:

        ::

            >>> pitches = "f' g'"
            >>> durations = [Duration(5, 8)]
            >>> leaves = scoretools.make_leaves(
            ...     pitches,
            ...     durations,
            ...     forbidden_written_duration=Duration(1, 2),
            ...     )
            >>> staff = Staff(leaves)
            >>> time_signature = TimeSignature((5, 4))
            >>> attach(time_signature, staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \time 5/4
                f'4 ~
                f'4 ~
                f'8
                g'4 ~
                g'4 ~
                g'8
            }

    ..  container:: example

        **Example 11.** You may set `forbidden_written_duration` and
        `decrease_durations_monotonically` together:

        ::

            >>> pitches = "f' g'"
            >>> durations = [Duration(5, 8)]
            >>> leaves = scoretools.make_leaves(
            ...     pitches,
            ...     durations,
            ...     forbidden_written_duration=Duration(1, 2),
            ...     decrease_durations_monotonically=False,
            ...     )
            >>> staff = Staff(leaves)
            >>> time_signature = TimeSignature((5, 4))
            >>> attach(time_signature, staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \time 5/4
                f'8 ~
                f'4 ~
                f'4
                g'8 ~
                g'4 ~
                g'4
            }

    ..  container:: example

        **Example 12.** Set `is_diminution` to true to produce
        diminished tuplets:

        ::

            >>> pitches = "f'"
            >>> durations = [Duration(5, 14)]
            >>> leaves = scoretools.make_leaves(
            ...     pitches,
            ...     durations,
            ...     is_diminution=True
            ...     )
            >>> staff = Staff(leaves)
            >>> time_signature = TimeSignature((5, 14))
            >>> attach(time_signature, staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \time 5/14
                \tweak edge-height #'(0.7 . 0)
                \times 4/7 {
                    f'2 ~
                    f'8
                }
            }

        This is default behavior.

    ..  container:: example

        **Example 13.** Set `is_diminution` to false to produce
        agumented tuplets:

        ::

            >>> pitches = "f'"
            >>> durations = [Duration(5, 14)]
            >>> leaves = scoretools.make_leaves(
            ...     pitches,
            ...     durations,
            ...     is_diminution=False
            ...     )
            >>> staff = Staff(leaves)
            >>> time_signature = TimeSignature((5, 14))
            >>> attach(time_signature, staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \time 5/14
                \tweak text #tuplet-number::calc-fraction-text
                \tweak edge-height #'(0.7 . 0)
                \times 8/7 {
                    f'4 ~
                    f'16
                }
            }

    ..  container:: example

        **Example 14.** None-valued elements in `pitches` result in
        multimeasure rests when the multimeasure rest keyword is set:

        ::

            >>> pitches = [None]
            >>> durations = [Duration(3, 8), Duration(5, 8)]
            >>> leaves = scoretools.make_leaves(
            ...     pitches,
            ...     durations,
            ...     use_multimeasure_rests=True,
            ...     )
            >>> leaves
            Selection([MultimeasureRest('R1 * 3/8'), MultimeasureRest('R1 * 5/8')])

        ::

            >>> staff = Staff([
            ...     Measure((3, 8), [leaves[0]]),
            ...     Measure((5, 8), [leaves[1]]),
            ...     ])
            >>> staff.context_name = 'RhythmicStaff'
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new RhythmicStaff {
                {
                    \time 3/8
                    R1 * 3/8
                }
                {
                    \time 5/8
                    R1 * 5/8
                }
            }

    ..  container:: example

        **Example 15.** Uses Messiaen-style ties:

        ::

            >>> pitches = [0]
            >>> durations = [Duration(13, 16)]
            >>> leaves = scoretools.make_leaves(
            ...     pitches,
            ...     durations,
            ...     use_messiaen_style_ties=True,
            ...     )
            >>> staff = Staff(leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'2.
                c'16 \repeatTie
            }

    ..  container:: example

        **Example 16.** Works with numbered pitch-class:

        ::

            >>> pitches = [pitchtools.NumberedPitchClass(6)]
            >>> durations = [Duration(13, 16)]
            >>> leaves = scoretools.make_leaves(
            ...     pitches,
            ...     durations,
            ...     )
            >>> staff = Staff(leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                fs'2. ~
                fs'16
            }

    Returns selection of leaves.
    '''
    from abjad.tools import scoretools
    if isinstance(pitches, str):
        pitches = pitches.split()
    if not isinstance(pitches, list):
        pitches = [pitches]
    if isinstance(durations, (numbers.Number, tuple)):
        durations = [durations]
    nonreduced_fractions = [mathtools.NonreducedFraction(_) for _ in durations]
    size = max(len(nonreduced_fractions), len(pitches))
    nonreduced_fractions = sequencetools.repeat_sequence_to_length(
        nonreduced_fractions, 
        size,
        )
    pitches = sequencetools.repeat_sequence_to_length(pitches, size)
    Duration = durationtools.Duration
    duration_groups = \
        Duration._group_nonreduced_fractions_by_implied_prolation(
        nonreduced_fractions)
    result = []
    for duration_group in duration_groups:
        # get factors in denominator of duration group other than 1, 2.
        factors = set(mathtools.factors(duration_group[0].denominator))
        factors.discard(1)
        factors.discard(2)
        current_pitches = pitches[0:len(duration_group)]
        pitches = pitches[len(duration_group):]
        if len(factors) == 0:
            for pitch, duration in zip(current_pitches, duration_group):
                leaves = _make_leaf_on_pitch(
                    pitch,
                    duration,
                    decrease_durations_monotonically=decrease_durations_monotonically,
                    forbidden_written_duration=forbidden_written_duration,
                    use_multimeasure_rests=use_multimeasure_rests,
                    use_messiaen_style_ties=use_messiaen_style_ties,
                    )
                result.extend(leaves)
        else:
            # compute tuplet prolation
            denominator = duration_group[0].denominator
            numerator = mathtools.greatest_power_of_two_less_equal(denominator)
            multiplier = (numerator, denominator)
            ratio = 1 / durationtools.Duration(*multiplier)
            duration_group = [ratio * durationtools.Duration(duration)
                for duration in duration_group]
            # make tuplet leaves
            tuplet_leaves = []
            for pitch, duration in zip(current_pitches, duration_group):
                leaves = _make_leaf_on_pitch(
                    pitch,
                    duration,
                    decrease_durations_monotonically=\
                        decrease_durations_monotonically,
                    use_multimeasure_rests=use_multimeasure_rests,
                    use_messiaen_style_ties=use_messiaen_style_ties,
                    )
                tuplet_leaves.extend(leaves)
            tuplet = scoretools.Tuplet(multiplier, tuplet_leaves)
            if is_diminution and not tuplet.is_diminution:
                tuplet.toggle_prolation()
            elif not is_diminution and tuplet.is_diminution:
                tuplet.toggle_prolation()
            result.append(tuplet)
    result = selectiontools.Selection(result)
    return result


def _make_leaf_on_pitch(
    pitch,
    duration,
    decrease_durations_monotonically=True,
    forbidden_written_duration=None,
    use_multimeasure_rests=False,
    use_messiaen_style_ties=False,
    ):
    from abjad.tools import scoretools
    note_prototype = (
        numbers.Number,
        str,
        pitchtools.NamedPitch,
        pitchtools.PitchClass,
        )
    chord_prototype = (tuple, list)
    rest_prototype = (type(None),)
    if isinstance(pitch, note_prototype):
        leaves = scoretools.make_tied_leaf(
            scoretools.Note,
            duration,
            decrease_durations_monotonically=decrease_durations_monotonically,
            forbidden_written_duration=forbidden_written_duration,
            pitches=pitch,
            use_messiaen_style_ties=use_messiaen_style_ties,
            )
    elif isinstance(pitch, chord_prototype):
        leaves = scoretools.make_tied_leaf(
            scoretools.Chord,
            duration,
            decrease_durations_monotonically=decrease_durations_monotonically,
            forbidden_written_duration=forbidden_written_duration,
            pitches=pitch,
            use_messiaen_style_ties=use_messiaen_style_ties,
            )
    elif isinstance(pitch, rest_prototype) and not use_multimeasure_rests:
        leaves = scoretools.make_tied_leaf(
            scoretools.Rest,
            duration,
            decrease_durations_monotonically=decrease_durations_monotonically,
            forbidden_written_duration=forbidden_written_duration,
            pitches=None,
            use_messiaen_style_ties=use_messiaen_style_ties,
            )
    elif isinstance(pitch, rest_prototype) and use_multimeasure_rests:
        multimeasure_rest = scoretools.MultimeasureRest((1))
        multiplier = durationtools.Multiplier(duration)
        attach(multiplier, multimeasure_rest)
        leaves = (
            multimeasure_rest,
            )
    else:
        message = 'unknown pitch {!r}.'
        message = message.format(pitch)
        raise ValueError(message)
    return leaves
