import abjad


def test_datastructuretools_TreeContainer_append_01():

    leaf_a = abjad.TreeNode()
    leaf_b = abjad.TreeNode()
    leaf_c = abjad.TreeNode()
    leaf_d = abjad.TreeNode()
    container = abjad.TreeContainer()

    assert container.children == ()

    container.append(leaf_a)
    assert container.children == (leaf_a,)

    container.append(leaf_b)
    assert container.children == (leaf_a, leaf_b)

    container.append(leaf_c)
    assert container.children == (leaf_a, leaf_b, leaf_c)

    container.append(leaf_d)
    assert container.children == (leaf_a, leaf_b, leaf_c, leaf_d)

    container.append(leaf_a)
    assert container.children == (leaf_b, leaf_c, leaf_d, leaf_a)
