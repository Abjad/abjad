# -*- coding: utf-8 -*-
from abjad import *


def test_quantizationtools_UnweightedSearchTree__find_leaf_subdivisions_01():

    definition = {
        2: {
            2: {
                2: None
            },
            3: None
        },
        5: None
    }
    search_tree = quantizationtools.UnweightedSearchTree(definition)

    assert search_tree._find_leaf_subdivisions((1, (1, 2))) == ((1, 1), (1, 1, 1))
    assert search_tree._find_leaf_subdivisions((1, (1, 2), (1, 2))) == ((1, 1),)
    assert search_tree._find_leaf_subdivisions((1, (1, 2), (1, 2), (1, 2))) == ()
    assert search_tree._find_leaf_subdivisions((1, (1, 2), (1, 3))) == ()
    assert search_tree._find_leaf_subdivisions((1, (1, 5))) == ()
