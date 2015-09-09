# -*- coding: utf-8 -*-
import pickle
from abjad.tools import datastructuretools


def test_datastructuretools_TreeContainer_pickle_01():

    container = datastructuretools.TreeContainer()
    leaf_a = datastructuretools.TreeNode()
    leaf_b = datastructuretools.TreeNode()
    leaf_c = datastructuretools.TreeNode()
    container.extend((leaf_a, leaf_b, leaf_c))

    pickled = pickle.loads(pickle.dumps(container))

    assert format(container) == format(pickled)
