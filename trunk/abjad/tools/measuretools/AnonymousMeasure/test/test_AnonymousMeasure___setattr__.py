from abjad import *
import py.test


def test_AnonymousMeasure___setattr___01( ):
   '''Slots constraint anonymous measure attributes.
   '''

   measure = measuretools.AnonymousMeasure(macros.scale(3))

   assert py.test.raises(AttributeError, "measure.foo = 'bar'")
