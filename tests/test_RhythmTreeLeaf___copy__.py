import copy

import abjad
import abjad.rhythmtrees


def test_RhythmTreeLeaf___copy___01():

    leaf = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=1)

    copied = copy.copy(leaf)

    assert format(leaf) == format(copied)
    assert leaf is not copied


def test_RhythmTreeLeaf___copy___02():

    leaf = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=2, is_pitched=True)

    copied = copy.copy(leaf)

    assert format(leaf) == format(copied)
    assert leaf is not copied
