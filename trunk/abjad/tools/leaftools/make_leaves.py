from __future__ import division
import numbers
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools import sequencetools


def make_leaves(pitches, durations, decrease_durations_monotonically=True, tie_rests=False,
    forbidden_written_duration=None):
    r'''.. versionadded:: 1.1

    Make leaves.

    Example 1. Integer and string elements in `pitches` result in notes:

    ::

        >>> leaves = leaftools.make_leaves([2, 4, 'F#5', 'G#5'], [Duration(1, 4)])
        >>> staff = Staff(leaves)

    ::

        >>> f(staff)
        \new Staff {
            d'4
            e'4
            fs''4
            gs''4
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Example 2. Tuple elements in `pitches` result in chords:

    ::

        >>> leaves = leaftools.make_leaves([(0, 2, 4), ('F#5', 'G#5', 'A#5')], [Duration(1, 2)])
        >>> staff = Staff(leaves)

    ::

        >>> f(staff)
        \new Staff {
            <c' d' e'>2
            <fs'' gs'' as''>2
        }

    ::
        
        >>> show(staff) # doctest: +SKIP

    Example 3. None-valued elements in `pitches` result in rests:

    ::

        >>> leaves = leaftools.make_leaves([None, None, None, None], [Duration(1, 4)])
        >>> staff = stafftools.RhythmicStaff(leaves)

    ::

        >>> f(staff)
        \new RhythmicStaff {
            r4
            r4
            r4
            r4
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Example 4. You can mix and match values passed to `pitches`:

    ::

        >>> leaves = leaftools.make_leaves([(0, 2, 4), None, 'C#5', 'D#5'], [Duration(1, 4)])
        >>> staff = Staff(leaves)

    ::

        >>> f(staff)
        \new Staff {
            <c' d' e'>4
            r4
            cs''4
            ds''4
        }

    ::
        
        >>> show(staff) # doctest: +SKIP

    Example 5. Read `pitches` cyclically when the length of `pitches`
    is less than the length of `durations`:
    
    ::

        >>> leaves = leaftools.make_leaves(['C5'], 2 * [Duration(3, 8), Duration(1, 8)])
        >>> staff = Staff(leaves)

    ::

        >>> f(staff)
        \new Staff {
            c''4.
            c''8
            c''4.
            c''8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Example 6. Read `durations` cyclically when the length of `durations`
    is less than the length of `pitches`:

    ::

        >>> leaves = leaftools.make_leaves("c'' d'' e'' f''", [Duration(1, 4)])
        >>> staff = Staff(leaves)

    ::

        >>> f(staff)
        \new Staff {
            c''4
            d''4
            e''4
            f''4
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Example 7. Elements in `durations` with non-power-of-two denominators
    result in tuplet-nested leaves:

    ::

        >>> leaves = leaftools.make_leaves(['D5'], 3 * [Duration(1, 3)])
        >>> staff = Staff(leaves)

    ::

        >>> f(staff)
        \new Staff {
            \times 2/3 {
                d''2
                d''2
                d''2
            }
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Example 8. Set `decrease_durations_monotonically` to true to return
    nonassignable durations tied from greatest to least:

    ::

        >>> leaves = leaftools.make_leaves(['D#5'], [Duration(13, 16)])
        >>> staff = Staff(leaves)
        >>> time_signature = contexttools.TimeSignatureMark((13, 16))(staff)

    ::

        >>> f(staff)
        \new Staff {
            \time 13/16
            ds''2. ~
            ds''16
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Example 9. Set `decrease_durations_monotonically` to false to return
    nonassignable durations tied from least to greatest:

    ::

        >>> leaves = leaftools.make_leaves(['E5'], [Duration(13, 16)], 
        ...     decrease_durations_monotonically=False)
        >>> staff = Staff(leaves)
        >>> time_signature = contexttools.TimeSignatureMark((13, 16))(staff)

    ::

        >>> f(staff)
        \new Staff {
            \time 13/16
            e''16 ~
            e''2.
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Example 10. Set `tie_rests` to true to return tied rests for nonassignable durations.
    Note that LilyPond does not engrave ties between rests:

    ::

        >>> leaves = leaftools.make_leaves([None], [Duration(5, 8)], tie_rests=True)
        >>> staff = stafftools.RhythmicStaff(leaves)
        >>> time_signature = contexttools.TimeSignatureMark((5, 8))(staff)

    ::

        >>> f(staff)
        \new RhythmicStaff {
            \time 5/8
            r2 ~
            r8
        }

    ::

        >>> show(staff) # doctest: +SKIP
    
    Example 11. Set `forbidden_written_duration` to avoid notes greater
    than or equal to a certain written duration:

    ::

        >>> leaves = leaftools.make_leaves("f' g'", [Duration(5, 8)],
        ...     forbidden_written_duration=Duration(1, 2))
        >>> staff = Staff(leaves)
        >>> time_signature = contexttools.TimeSignatureMark((5, 4))(staff)

    ::

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

    ::

        >>> show(staff) # doctest: +SKIP

    Example 12. You may set `forbidden_written_duration` and
    `decrease_durations_monotonically` together:

    ::

        >>> leaves = leaftools.make_leaves("f' g'", [Duration(5, 8)],
        ...     forbidden_written_duration=Duration(1, 2),
        ...     decrease_durations_monotonically=False)
        >>> staff = Staff(leaves)
        >>> time_signature = contexttools.TimeSignatureMark((5, 4))(staff)

    ::

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

    ::

        >>> show(staff) # doctest: +SKIP

    Return list of leaves.
    '''
    from abjad.tools import chordtools
    from abjad.tools import notetools
    from abjad.tools import resttools
    from abjad.tools import tuplettools

    def _make_leaf_on_pitch(pitch, duration,
        decrease_durations_monotonically=decrease_durations_monotonically):
        if isinstance(pitch, (numbers.Number, str, pitchtools.NamedChromaticPitch)):
            leaves = notetools.make_tied_note(pitch, duration,
                decrease_durations_monotonically=decrease_durations_monotonically,
                forbidden_written_duration=forbidden_written_duration)
        elif isinstance(pitch, (tuple, list)):
            leaves = chordtools.make_tied_chord(pitch, duration,
                decrease_durations_monotonically=decrease_durations_monotonically,
                forbidden_written_duration=forbidden_written_duration)
        elif pitch is None:
            leaves = resttools.make_tied_rest(duration,
                decrease_durations_monotonically=decrease_durations_monotonically,
                forbidden_written_duration=forbidden_written_duration,
                tie_parts=tie_rests)
        else:
            raise ValueError('Unknown pitch {!r}.'.format(pitch))
        return leaves

    if isinstance(pitches, str):
        pitches = pitches.split()

    if not isinstance(pitches, list):
        pitches = [pitches]

    if isinstance(durations, (numbers.Number, tuple)):
        durations = [durations]

    # make duration pairs
    duration_pairs = [durationtools.Duration(duration) for duration in durations]

    # set lists of pitches and duration pairs to the same length
    size = max(len(duration_pairs), len(pitches))
    duration_pairs = sequencetools.repeat_sequence_to_length(duration_pairs, size)
    pitches = sequencetools.repeat_sequence_to_length(pitches, size)

    duration_groups = durationtools.group_nonreduced_fractions_by_implied_prolation(duration_pairs)

    result = []
    for duration_group in duration_groups:
        # get factors in denominator of duration group other than 1, 2.
        factors = set(mathtools.factors(duration_group[0].denominator))
        factors.discard(1)
        factors.discard(2)
        ps = pitches[0:len(duration_group)]
        pitches = pitches[len(duration_group):]
        if len(factors) == 0:
            for pitch, duration in zip(ps, duration_group):
                leaves = _make_leaf_on_pitch(pitch, duration,
                    decrease_durations_monotonically=decrease_durations_monotonically)
                result.extend(leaves)
        else:
            # compute prolation
            denominator = duration_group[0].denominator
            numerator = mathtools.greatest_power_of_two_less_equal(denominator)
            multiplier = (numerator, denominator)
            ratio = 1 / durationtools.Duration(*multiplier)
            duration_group = [ratio * durationtools.Duration(duration) for duration in duration_group]
            # make leaves
            leaves = []
            for pitch, duration in zip(ps, duration_group):
                leaves.extend(_make_leaf_on_pitch(pitch, duration,
                    decrease_durations_monotonically=decrease_durations_monotonically))
            tuplet = tuplettools.Tuplet(multiplier, leaves)
            result.append(tuplet)

    return result
