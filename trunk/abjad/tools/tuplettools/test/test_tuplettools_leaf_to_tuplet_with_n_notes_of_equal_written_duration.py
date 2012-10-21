from abjad import *


def test_tuplettools_leaf_to_tuplet_with_n_notes_of_equal_written_duration_01():
    '''Divide a leaf of 3/16 into 1, ..., 5 parts.'''

    t = tuplettools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(Note("c'8."), 1, is_diminution=False)
    assert t.lilypond_format == "{\n\tc'8.\n}"

    t = tuplettools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(Note("c'8."), 2, is_diminution=False)
    assert t.lilypond_format == "{\n\tc'16.\n\tc'16.\n}"

    t = tuplettools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(Note("c'8."), 3, is_diminution=False)
    assert t.lilypond_format == "{\n\tc'16\n\tc'16\n\tc'16\n}"

    t = tuplettools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(Note("c'8."), 4, is_diminution=False)
    assert t.lilypond_format == "{\n\tc'32.\n\tc'32.\n\tc'32.\n\tc'32.\n}"

    t = tuplettools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(Note("c'8."), 5, is_diminution=False)
    assert t.lilypond_format == "\\fraction \\times 8/5 {\n\tc'64.\n\tc'64.\n\tc'64.\n\tc'64.\n\tc'64.\n}"


def test_tuplettools_leaf_to_tuplet_with_n_notes_of_equal_written_duration_02():
    '''Divide a leaf of 3/16 into 1, ..., 5 parts.'''

    t = tuplettools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(Note("c'8."), 1, is_diminution=True)
    assert t.lilypond_format == "{\n\tc'8.\n}"

    t = tuplettools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(Note("c'8."), 2, is_diminution=True)
    assert t.lilypond_format == "{\n\tc'16.\n\tc'16.\n}"

    t = tuplettools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(Note("c'8."), 3, is_diminution=True)
    assert t.lilypond_format == "{\n\tc'16\n\tc'16\n\tc'16\n}"

    t = tuplettools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(Note("c'8."), 4, is_diminution=True)
    assert t.lilypond_format == "{\n\tc'32.\n\tc'32.\n\tc'32.\n\tc'32.\n}"

    # TODO: DECIDE ON DOTTED VALUES #
    #t = tuplettools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(Note("c'8."), 5, is_diminution=True)
    #assert t.lilypond_format == "\\fraction \\times 3/5 {\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n}"
