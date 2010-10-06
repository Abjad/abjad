from abjad import *
import py.test
py.test.skip('unskip test after removing casting code.')


def test_foo_01( ):
   '''Slots constrain note attributes.
   '''

   note = Note(0, (1, 4))

   assert py.test.raises(AttributeError, "note.foo = 'bar'")
