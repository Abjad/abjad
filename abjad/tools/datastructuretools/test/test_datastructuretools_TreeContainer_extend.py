import abjad


def test_datastructuretools_TreeContainer_extend_01():

    leaf_a = abjad.TreeNode()
    leaf_b = abjad.TreeNode()
    leaf_c = abjad.TreeNode()
    leaf_d = abjad.TreeNode()

    container = abjad.TreeContainer()

    assert container.children == ()

    container.extend([leaf_a])
    assert container.children == (leaf_a,)

    container.extend([leaf_b, leaf_c, leaf_d])
    assert container.children == (leaf_a, leaf_b, leaf_c, leaf_d)

    container.extend([leaf_a, leaf_c])
    assert container.children == (leaf_b, leaf_d, leaf_a, leaf_c)
