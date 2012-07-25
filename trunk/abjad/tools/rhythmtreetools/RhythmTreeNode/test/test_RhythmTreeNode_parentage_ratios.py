from abjad.tools import rhythmtreetools


def test_RhythmTreeNode_parentage_ratios_01():

    string = '(1 (1 (2 (3 4)) 2))'
    tree = rhythmtreetools.RhythmTreeParser()(string)[0]

    assert tree.parentage_ratios == (1,)
    assert tree[0].parentage_ratios == ((1, 5), 1)
    assert tree[1].parentage_ratios == ((2, 5), 1)
    assert tree[1][0].parentage_ratios == ((3, 7), (2, 5), 1)
    assert tree[1][1].parentage_ratios == ((4, 7), (2, 5), 1)
    assert tree[2].parentage_ratios == ((2, 5), 1)
