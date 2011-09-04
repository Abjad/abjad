from abjad.tools import sequencetools
from abjad.tools.pitcharraytools.PitchArray import PitchArray
from abjad.tools.pitchtools.list_named_chromatic_pitches_in_expr import list_named_chromatic_pitches_in_expr


def _leaf_iterables_to_pitch_array(leaf_iterables, populate = True):
    r'''.. versionadded:: 2.0
    '''

    from abjad.tools import leaftools
    from abjad.tools import notetools
    from abjad.tools import componenttools

    time_intervals = leaftools.get_composite_offset_difference_series_from_leaves_in_expr(
        leaf_iterables)
    array_width = len(time_intervals)
    array_depth = len(leaf_iterables)
    pitch_array = PitchArray(array_depth, array_width)

    tokens = notetools.make_quarter_notes_with_lilypond_multipliers([0], time_intervals)
    for leaf_iterable, pitch_array_row in zip(leaf_iterables, pitch_array.rows):
        durations = leaftools.list_prolated_durations_of_leaves_in_expr(leaf_iterable)
        parts = componenttools.split_components_once_by_prolated_durations_and_do_not_fracture_crossing_spanners(
            tokens, durations)
        part_lengths = [len(part) for part in parts]
        cells = pitch_array_row.cells
        grouped_cells = sequencetools.partition_sequence_once_by_counts_without_overhang(cells, part_lengths)
        for group in grouped_cells:
            pitch_array_row.merge(group)
        leaves = leaftools.iterate_leaves_forward_in_expr(leaf_iterable)
        if populate:
            for cell, leaf in zip(pitch_array_row.cells, leaves):
                cell.pitches.extend(list_named_chromatic_pitches_in_expr(leaf))

    return pitch_array
