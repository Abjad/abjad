from abjad import *
import py.test


def test_Measure___setattr___01( ):
   '''Slots constraint measure attributes.
   '''

   measure = Measure((3, 8), macros.scale(3))

   assert py.test.raises(AttributeError, "measure.foo = 'bar'")
