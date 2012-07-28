from experimental import quantizationtools


def test_SimpleSearchTree_find_leaf_subdivisions_01():

    definition = {
        2: {
            2: {
                2: None
            }, 
            3: None
        }, 
        5: None
    }
    search_tree = quantizationtools.SimpleSearchTree(definition)

    assert search_tree.find_leaf_subdivisions((1, (1, 2))) == (2, 3)
    assert search_tree.find_leaf_subdivisions((1, (1, 2), (1, 2))) == (2,)
    assert search_tree.find_leaf_subdivisions((1, (1, 2), (1, 2), (1, 2))) == ()
    assert search_tree.find_leaf_subdivisions((1, (1, 2), (1, 3))) == ()
    assert search_tree.find_leaf_subdivisions((1, (1, 5))) == ()
