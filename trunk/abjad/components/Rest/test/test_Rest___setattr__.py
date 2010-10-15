from abjad import *
import py.test
py.test.skip('not yet implemented')


def test_Rest___setattr___01( ):

   rest = Rest((1, 4))

   assert py.test.raises(AttributeError, "rest.foo = 'bar'")
