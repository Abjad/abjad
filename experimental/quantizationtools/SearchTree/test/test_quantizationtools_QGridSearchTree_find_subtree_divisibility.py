from experimental.quantizationtools import SearchTree


def test_quantizationtools_QGridSearchTree_find_subtree_divisibility_01():
    qst = SearchTree({2: {2: {2: None}, 3: None}, 5: None})
    assert qst.find_subtree_divisibility((2,)) == (2, 3)
    assert qst.find_subtree_divisibility((5,)) == tuple([])
    assert qst.find_subtree_divisibility((2, 2)) == (2,)
    assert qst.find_subtree_divisibility((2, 3)) == tuple([])
