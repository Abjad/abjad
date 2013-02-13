from abjad.tools import rhythmtreetools
import copy


def test_RhythmTreeLeaf___copy___01():

    leaf = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=1)

    copied = copy.copy(leaf)

    assert leaf == copied
    assert leaf is not copied


def test_RhythmTreeLeaf___copy___02():

    leaf = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=2, is_pitched=True)

    copied = copy.copy(leaf)

    assert leaf == copied
    assert leaf is not copied
