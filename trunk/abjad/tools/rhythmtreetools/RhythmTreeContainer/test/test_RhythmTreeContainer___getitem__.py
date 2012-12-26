from abjad import *
import py.test


def test_RhythmTreeContainer___getitem___01():

    leaf_a = rhythmtreetools.RhythmTreeLeaf(duration=3)
    leaf_b = rhythmtreetools.RhythmTreeLeaf(duration=2)
    leaf_c = rhythmtreetools.RhythmTreeLeaf(duration=1)

    container = rhythmtreetools.RhythmTreeContainer(duration=1, children=[leaf_a, leaf_b, leaf_c])

    assert container[0] is leaf_a
    assert container[1] is leaf_b
    assert container[2] is leaf_c

    py.test.raises(Exception, 'container[3]')

    assert container[-1] is leaf_c
    assert container[-2] is leaf_b
    assert container[-3] is leaf_a

    py.test.raises(Exception, 'container[-4]')
