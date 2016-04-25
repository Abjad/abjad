# -*- coding: utf-8 -*-
from abjad.tools import rhythmtreetools
import pickle


def test_rhythmtreetools_RhythmTreeNode_pickle_01():

    string = '(1 (1 (2 (1 1 1)) 2))'
    tree = rhythmtreetools.RhythmTreeParser()(string)[0]

    pickled = pickle.loads(pickle.dumps(tree))

    assert format(pickled) == format(tree)
    assert pickled != tree
    assert pickled is not tree
