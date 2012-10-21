from abjad import *


def test_tuplettools_leaf_to_tuplet_with_ratio_01():

    note = Note(0, (3, 16))

    t = tuplettools.leaf_to_tuplet_with_ratio(note, [1], is_diminution=False)
    assert t.lilypond_format == "{\n\tc'8.\n}"

    t = tuplettools.leaf_to_tuplet_with_ratio(note, [1, 2], is_diminution=False)
    assert t.lilypond_format == "{\n\tc'16\n\tc'8\n}"

    # TODO: DECIDE ON DOTTED VALUES #
    #t = tuplettools.leaf_to_tuplet_with_ratio(note, [1, 2, 2], is_diminution=False)
    #assert t.lilypond_format == "\\fraction \\times 6/5 {\n\tc'32\n\tc'16\n\tc'16\n}"

    t = tuplettools.leaf_to_tuplet_with_ratio(note, [1, 2, 2, 3], is_diminution=False)
    assert t.lilypond_format == "\\fraction \\times 3/2 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n}"

    t = tuplettools.leaf_to_tuplet_with_ratio(note, [1, 2, 2, 3, 3], is_diminution=False)
    assert t.lilypond_format == "\\fraction \\times 12/11 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n\tc'32.\n}"

    t = tuplettools.leaf_to_tuplet_with_ratio(note, [1, 2, 2, 3, 3, 4], is_diminution=False)
    assert t.lilypond_format == "\\fraction \\times 8/5 {\n\tc'128\n\tc'64\n\tc'64\n\tc'64.\n\tc'64.\n\tc'32\n}"


def test_tuplettools_leaf_to_tuplet_with_ratio_02():

    note = Note(0, (3, 16))

    t = tuplettools.leaf_to_tuplet_with_ratio(note, [1], is_diminution=True)
    assert t.lilypond_format == "{\n\tc'8.\n}"

    t = tuplettools.leaf_to_tuplet_with_ratio(note, [1, 2], is_diminution=True)
    assert t.lilypond_format == "{\n\tc'16\n\tc'8\n}"

    # TODO: DECIDE ON DOTTED VALUES #
    #t = tuplettools.leaf_to_tuplet_with_ratio(note, [1, 2, 2], is_diminution=True)
    #assert t.lilypond_format == "\\fraction \\times 3/5 {\n\tc'16\n\tc'8\n\tc'8\n}"

    t = tuplettools.leaf_to_tuplet_with_ratio(note, [1, 2, 2, 3], is_diminution=True)
    assert t.lilypond_format == "\\fraction \\times 3/4 {\n\tc'32\n\tc'16\n\tc'16\n\tc'16.\n}"

    t = tuplettools.leaf_to_tuplet_with_ratio(note, [1, 2, 2, 3, 3], is_diminution=True)
    assert t.lilypond_format == "\\fraction \\times 6/11 {\n\tc'32\n\tc'16\n\tc'16\n\tc'16.\n\tc'16.\n}"

    t = tuplettools.leaf_to_tuplet_with_ratio(note, [1, 2, 2, 3, 3, 4], is_diminution=True)
    assert t.lilypond_format == "\\times 4/5 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n\tc'32.\n\tc'16\n}"
