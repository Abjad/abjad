from abjad import *
import py.test


def test_Tuplet___setattr___01( ):
   '''Slots constrain tuplet attributes.
   '''

   tuplet = Tuplet((2, 3), macros.scale(3))

   assert py.test.raises(AttributeError, "tuplet.foo = 'bar'")
