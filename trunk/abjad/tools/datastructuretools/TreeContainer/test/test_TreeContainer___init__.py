from abjad import *


def test_TreeContainer___init___01():

    container = datastructuretools.TreeContainer()

    assert container.children == ()
    assert container.parent is None
