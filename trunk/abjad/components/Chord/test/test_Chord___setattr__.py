from abjad import *
import py.test
py.test.skip('not yet implemented')


def test_Chord___setattr___01( ):

   chord = Chord([3, 13, 17], (1, 4))

   assert py.test.raises(AttributeError, "chord.foo = 'bar'")
