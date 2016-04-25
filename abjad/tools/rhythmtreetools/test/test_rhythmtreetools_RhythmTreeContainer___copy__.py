# -*- coding: utf-8 -*-
from abjad.tools import rhythmtreetools
import copy


def test_rhythmtreetools_RhythmTreeContainer___copy___01():

    string = '(1 (1 (2 (3 (4 (1 1 1)))) 2))'
    tree = rhythmtreetools.RhythmTreeParser()(string)[0]
    copied = copy.copy(tree)

    assert format(tree) == format(copied)
    assert tree is not copied

    assert format(tree[0]) == format(copied[0])
    assert tree[0] is not copied[0]

    assert format(tree[1]) == format(copied[1])
    assert tree[1] is not copied[1]

    assert format(tree[2]) == format(copied[2])
    assert tree[2] is not copied[2]
