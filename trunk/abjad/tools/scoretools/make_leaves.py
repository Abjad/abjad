# -*- encoding: utf-8 -*-
from __future__ import division
import numbers
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools import selectiontools
from abjad.tools import sequencetools


def make_leaves(
    pitches,
    durations,
    decrease_durations_monotonically=True,
    tie_rests=False,
    forbidden_written_duration=None,
    metrical_hiearchy=None,
    ):
    r'''Make leaves.

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
            >>> staff = scoretools.RhythmicStaff(leaves)
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
            >>> time_signature = contexttools.TimeSignatureMark((13, 16))
            >>> time_signature = attach(time_signature, staff)
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
            >>> time_signature = contexttools.TimeSignatureMark((13, 16))
            >>> time_signature = attach(time_signature, staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \time 13/16
                e''16 ~
                e''2.
            }

    ..  container:: example
        
        **Example 10.** Set `tie_rests` to true to return tied rests for 
        nonassignable durations. Note that LilyPond does not engrave 
        ties between rests:

        ::

            >>> pitches = [None]
            >>> durations = [Duration(5, 8)]
            >>> leaves = scoretools.make_leaves(
            ...     pitches, 
            ...     durations, 
            ...     tie_rests=True,
            ...     )
            >>> staff = scoretools.RhythmicStaff(leaves)
            >>> time_signature = contexttools.TimeSignatureMark((5, 8))
            >>> time_signature = attach(time_signature, staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new RhythmicStaff {
                \time 5/8
                r2 ~
                r8
            }

    ..  container:: example
    
        **Example 11.** Set `forbidden_written_duration` to avoid notes 
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
            >>> time_signature = contexttools.TimeSignatureMark((5, 4))
            >>> time_signature = attach(time_signature, staff)
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
        
        **Example 12.** You may set `forbidden_written_duration` and
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
            >>> time_signature = contexttools.TimeSignatureMark((5, 4))
            >>> time_siganture = attach(time_signature, staff)
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

    Returns selection of unincorporated leaves.
    '''
    from abjad.tools import scoretools
    from abjad.tools import scoretools
    from abjad.tools import scoretools
    from abjad.tools import scoretools

    if isinstance(pitches, str):
        pitches = pitches.split()

    if not isinstance(pitches, list):
        pitches = [pitches]

    if isinstance(durations, (numbers.Number, tuple)):
        durations = [durations]

    # make duration pairs
    duration_pairs = [durationtools.Duration(duration) 
        for duration in durations]

    # set lists of pitches and duration pairs to the same length
    size = max(len(duration_pairs), len(pitches))
    duration_pairs = \
        sequencetools.repeat_sequence_to_length(duration_pairs, size)
    pitches = sequencetools.repeat_sequence_to_length(pitches, size)

    Duration = durationtools.Duration
    duration_groups = \
        Duration._group_nonreduced_fractions_by_implied_prolation(
        duration_pairs)

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
                    tie_rests=tie_rests,
                    )
                result.extend(leaves)
        else:
            # compute tuplet prolation
            denominator = duration_group[0].denominator
            numerator = \
                mathtools.greatest_power_of_two_less_equal(denominator)
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
                    decrease_durations_monotonically=decrease_durations_monotonically,
                    )
                tuplet_leaves.extend(leaves)
            tuplet = scoretools.Tuplet(multiplier, tuplet_leaves)
            result.append(tuplet)

    result = selectiontools.Selection(result)
    return result


def _make_leaf_on_pitch(
    pitch,
    duration,
    decrease_durations_monotonically=True,
    forbidden_written_duration=None,
    tie_rests=False,
    ):
    from abjad.tools import scoretools
    from abjad.tools import scoretools
    from abjad.tools import scoretools
    from abjad.tools import scoretools
    note_types = (numbers.Number, str, pitchtools.NamedPitch)
    chord_types = (tuple, list)
    rest_types = (type(None),)
    if isinstance(pitch, note_types):
        leaves = scoretools.make_tied_leaf(
            scoretools.Note,
            duration,
            decrease_durations_monotonically=decrease_durations_monotonically,
            forbidden_written_duration=forbidden_written_duration,
            pitches=pitch,
            )
    elif isinstance(pitch, chord_types):
        leaves = scoretools.make_tied_leaf(
            scoretools.Chord,
            duration,
            decrease_durations_monotonically=decrease_durations_monotonically,
            forbidden_written_duration=forbidden_written_duration,
            pitches=pitch,
            )
    elif isinstance(pitch, rest_types):
        leaves = scoretools.make_tied_leaf(
            scoretools.Rest,
            duration,
            decrease_durations_monotonically=decrease_durations_monotonically,
            forbidden_written_duration=forbidden_written_duration,
            pitches=None,
            tie_parts=tie_rests,
            )
    else:
        message = 'unknown pitch {!r}.'.format(pitch)
        raise ValueError(message)

    return leaves
