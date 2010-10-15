from abjad import *
import py.test
py.test.skip('not yet implemented')


def test_Skip___setattr___01( ):

   skip = Skip((1, 4))

   assert py.test.raises(AttributeError, "skip.foo = 'bar'")
