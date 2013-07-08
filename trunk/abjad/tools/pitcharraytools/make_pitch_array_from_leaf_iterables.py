from abjad.tools import componenttools
from abjad.tools import iterationtools
from abjad.tools import leaftools
from abjad.tools import notetools
from abjad.tools import pitchtools
from abjad.tools import sequencetools


def make_pitch_array_from_leaf_iterables(leaf_iterables, populate=True):
    r'''.. versionadded:: 2.0

    Make pitch array from `leaf_iterables`.

    Example 1. Make empty pitch array from score:

    ::

        >>> score = Score([])
        >>> score.append(Staff("c'8 d'8 e'8 f'8"))
        >>> score.append(Staff("c'4 d'4"))
        >>> score.append(
        ...     Staff(
        ...     tuplettools.FixedDurationTuplet(
        ...     Duration(2, 8), "c'8 d'8 e'8") * 2))

    ::

        >>> f(score)
        \new Score <<
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
            \new Staff {
                c'4
                d'4
            }
            \new Staff {
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }
            }
        >>

    ::

        >>> array = pitcharraytools.make_pitch_array_from_leaf_iterables(
        ...     score, populate=False)
        >>> print array
        [     ] [     ] [     ] [     ]
        [                 ] [                 ]
        [ ] [     ] [ ] [ ] [     ] [ ]

    Example 2. Make populated pitch array from `leaf_iterables`:

    ::

        >>> score = Score([])
        >>> score.append(Staff("c'8 d'8 e'8 f'8"))
        >>> score.append(Staff("c'4 d'4"))
        >>> score.append(
        ...     Staff(
        ...     tuplettools.FixedDurationTuplet(
        ...     Duration(2, 8), "c'8 d'8 e'8") * 2))

    ::

        >>> f(score)
        \new Score <<
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
            \new Staff {
                c'4
                d'4
            }
            \new Staff {
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }
            }
        >>

    ::

        >>> array = pitcharraytools.make_pitch_array_from_leaf_iterables(
        ...     score, populate=True)
        >>> print array
        [c'     ] [d'     ] [e'     ] [f'     ]
        [c'                   ] [d'                   ]
        [c'] [d'     ] [e'] [c'] [d'     ] [e']
 
    Return pitch array.
    '''
    from abjad.tools import pitcharraytools

    time_intervals = \
        leaftools.get_composite_offset_difference_series_from_leaves_in_expr(
        leaf_iterables)
    array_width = len(time_intervals)
    array_depth = len(leaf_iterables)
    pitch_array = pitcharraytools.PitchArray(array_depth, array_width)

    tokens = notetools.make_quarter_notes_with_lilypond_multipliers(
        [0], time_intervals)
    for leaf_iterable, pitch_array_row in \
        zip(leaf_iterables, pitch_array.rows):
        durations = leaftools.list_durations_of_leaves_in_expr(leaf_iterable)
        parts = componenttools.split_components_at_offsets(
            tokens, durations, cyclic=False, fracture_spanners=False)
        part_lengths = [len(part) for part in parts]
        cells = pitch_array_row.cells
        grouped_cells = sequencetools.partition_sequence_by_counts(
            cells, part_lengths, cyclic=False, overhang=False)
        for group in grouped_cells:
            pitch_array_row.merge(group)
        leaves = iterationtools.iterate_leaves_in_expr(leaf_iterable)
        if populate:
            for cell, leaf in zip(pitch_array_row.cells, leaves):
                cell.pitches.extend(
                    pitchtools.list_named_chromatic_pitches_in_expr(leaf))
    return pitch_array
