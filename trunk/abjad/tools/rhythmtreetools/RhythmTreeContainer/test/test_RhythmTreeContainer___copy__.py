from abjad.tools import rhythmtreetools
import copy


def test_RhythmTreeContainer___copy___01():

    string = '(1 (1 (2 (3 (4 (1 1 1)))) 2))'
    tree = rhythmtreetools.RhythmTreeParser()(string)[0]
    copied = copy.copy(tree)

    assert tree == copied
    assert tree is not copied

    assert tree[0] == copied[0]
    assert tree[0] is not copied[0]

    assert tree[1] == copied[1]
    assert tree[1] is not copied[1]

    assert tree[2] == copied[2]
    assert tree[2] is not copied[2]

