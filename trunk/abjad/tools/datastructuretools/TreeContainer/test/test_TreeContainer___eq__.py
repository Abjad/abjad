from abjad.tools import datastructuretools


def test_TreeContainer___eq___01():

    a = datastructuretools.TreeContainer([])
    b = datastructuretools.TreeContainer([])

    assert a == b


def test_TreeContainer___eq___02():

    a = datastructuretools.TreeContainer([
        datastructuretools.TreeNode()
        ])
    b = datastructuretools.TreeContainer([
        datastructuretools.TreeNode()
        ])

    assert a == b


def test_TreeContainer___eq___03():

    a = datastructuretools.TreeContainer([])
    b = datastructuretools.TreeContainer([
        datastructuretools.TreeNode()
        ])
    c = datastructuretools.TreeContainer([
        datastructuretools.TreeNode(),
        datastructuretools.TreeNode()
        ])

    assert a != b
    assert a != c
    assert b != c

