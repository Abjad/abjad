import abjad


def test_datastructuretools_TreeContainer___iter___01():

    leaf_a = abjad.TreeNode()
    leaf_b = abjad.TreeNode()
    leaf_c = abjad.TreeNode()

    container = abjad.TreeContainer([leaf_a, leaf_b, leaf_c])

    assert [x for x in container] == [leaf_a, leaf_b, leaf_c]
