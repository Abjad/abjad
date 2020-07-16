import pickle

import abjad
import abjad.rhythmtrees


def test_RhythmTreeNode_pickle_01():

    string = "(1 (1 (2 (1 1 1)) 2))"
    tree = abjad.rhythmtrees.RhythmTreeParser()(string)[0]

    pickled = pickle.loads(pickle.dumps(tree))

    assert abjad.storage(pickled) == abjad.storage(tree)
    assert pickled != tree
    assert pickled is not tree
