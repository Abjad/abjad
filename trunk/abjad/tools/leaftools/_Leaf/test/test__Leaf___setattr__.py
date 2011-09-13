from abjad import *
from abjad.tools.leaftools._Leaf import _Leaf
import py.test


def test__Leaf___setattr___01():
    '''Slots constrain leaf attributes.
    '''

    leaf = _Leaf(Duration(1, 4))

    assert py.test.raises(AttributeError, "leaf.foo = 'bar'")
