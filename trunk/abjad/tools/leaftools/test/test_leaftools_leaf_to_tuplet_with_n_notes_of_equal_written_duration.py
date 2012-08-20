from abjad import *


def test_leaftools_leaf_to_tuplet_with_n_notes_of_equal_written_duration_99():
    '''Divide a leaf of 3/16 into 1, ..., 5 parts.'''

    t = leaftools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(Note("c'8."), 1, diminution=False)
    assert t.lilypond_format == "{\n\tc'8.\n}"

    t = leaftools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(Note("c'8."), 2, diminution=False)
    assert t.lilypond_format == "{\n\tc'16.\n\tc'16.\n}"

    t = leaftools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(Note("c'8."), 3, diminution=False)
    assert t.lilypond_format == "{\n\tc'16\n\tc'16\n\tc'16\n}"

    t = leaftools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(Note("c'8."), 4, diminution=False)
    assert t.lilypond_format == "{\n\tc'32.\n\tc'32.\n\tc'32.\n\tc'32.\n}"

    t = leaftools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(Note("c'8."), 5, diminution=False)
    assert t.lilypond_format == "\\fraction \\times 8/5 {\n\tc'64.\n\tc'64.\n\tc'64.\n\tc'64.\n\tc'64.\n}"


def test_leaftools_leaf_to_tuplet_with_n_notes_of_equal_written_duration_98():
    '''Divide a leaf of 3/16 into 1, ..., 5 parts.'''

    t = leaftools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(Note("c'8."), 1, diminution=True)
    assert t.lilypond_format == "{\n\tc'8.\n}"

    t = leaftools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(Note("c'8."), 2, diminution=True)
    assert t.lilypond_format == "{\n\tc'16.\n\tc'16.\n}"

    t = leaftools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(Note("c'8."), 3, diminution=True)
    assert t.lilypond_format == "{\n\tc'16\n\tc'16\n\tc'16\n}"

    t = leaftools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(Note("c'8."), 4, diminution=True)
    assert t.lilypond_format == "{\n\tc'32.\n\tc'32.\n\tc'32.\n\tc'32.\n}"

    # TODO: DECIDE ON DOTTED VALUES #
    #t = leaftools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(Note("c'8."), 5, diminution=True)
    #assert t.lilypond_format == "\\fraction \\times 3/5 {\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n}"
