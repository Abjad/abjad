from abjad import *
from abjad.components._Leaf import _Leaf
import py.test
py.test.skip('unskip test after removing casting code.')


def test__Leaf___setattr___01( ):
   '''Slots constrain leaf attributes.
   '''

   _leaf = _Leaf(Fraction(1, 4))

   assert py.test.raises(AttributeError, "_leaf.foo = 'bar'")
