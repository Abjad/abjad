from abjad import *


def test_leaftools_leaf_to_diminished_tuplet_with_n_notes_of_equal_written_duration_01():
    '''Divide a leaf of 3/16 into 1, ..., 5 parts.'''

    t = leaftools.leaf_to_diminished_tuplet_with_n_notes_of_equal_written_duration(Note(0, (3, 16)), 1)
    assert t.format == "{\n\tc'8.\n}"

    t = leaftools.leaf_to_diminished_tuplet_with_n_notes_of_equal_written_duration(Note(0, (3, 16)), 2)
    assert t.format == "{\n\tc'16.\n\tc'16.\n}"

    t = leaftools.leaf_to_diminished_tuplet_with_n_notes_of_equal_written_duration(Note(0, (3, 16)), 3)
    assert t.format == "{\n\tc'16\n\tc'16\n\tc'16\n}"

    t = leaftools.leaf_to_diminished_tuplet_with_n_notes_of_equal_written_duration(Note(0, (3, 16)), 4)
    assert t.format == "{\n\tc'32.\n\tc'32.\n\tc'32.\n\tc'32.\n}"

    # TODO: DECIDE ON DOTTED VALUES #
    #t = leaftools.leaf_to_diminished_tuplet_with_n_notes_of_equal_written_duration(Note(0, (3, 16)), 5)
    #assert t.format == "\\fraction \\times 3/5 {\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n}"
