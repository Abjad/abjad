from abjad import *
import py.test


def test_DynamicMeasure___setattr___01( ):
   '''Slots constraint dynamic measure attributes.
   '''

   measure = measuretools.DynamicMeasure(macros.scale(3))

   assert py.test.raises(AttributeError, "measure.foo = 'bar'")
