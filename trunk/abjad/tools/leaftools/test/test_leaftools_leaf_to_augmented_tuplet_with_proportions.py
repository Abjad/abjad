from abjad import *


def test_leaftools_leaf_to_augmented_tuplet_with_proportions_01():

    note = Note(0, (3, 16))

    t = leaftools.leaf_to_augmented_tuplet_with_proportions(note, [1])
    assert t.format == "{\n\tc'8.\n}"

    t = leaftools.leaf_to_augmented_tuplet_with_proportions(note, [1, 2])
    assert t.format == "{\n\tc'16\n\tc'8\n}"

    # TODO: DECIDE ON DOTTED VALUES #
    #t = leaftools.leaf_to_augmented_tuplet_with_proportions(note, [1, 2, 2])
    #assert t.format == "\\fraction \\times 6/5 {\n\tc'32\n\tc'16\n\tc'16\n}"

    t = leaftools.leaf_to_augmented_tuplet_with_proportions(note, [1, 2, 2, 3])
    assert t.format == "\\fraction \\times 3/2 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n}"

    t = leaftools.leaf_to_augmented_tuplet_with_proportions(note, [1, 2, 2, 3, 3])
    assert t.format == "\\fraction \\times 12/11 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n\tc'32.\n}"

    t = leaftools.leaf_to_augmented_tuplet_with_proportions(note, [1, 2, 2, 3, 3, 4])
    assert t.format == "\\fraction \\times 8/5 {\n\tc'128\n\tc'64\n\tc'64\n\tc'64.\n\tc'64.\n\tc'32\n}"
