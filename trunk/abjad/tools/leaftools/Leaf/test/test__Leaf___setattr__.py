from abjad import *
from abjad.tools.leaftools.Leaf import Leaf
import py.test


def test_Leaf___setattr___01():
    '''Slots constrain leaf attributes.
    '''

    leaf = Leaf(Duration(1, 4))

    assert py.test.raises(AttributeError, "leaf.foo = 'bar'")
