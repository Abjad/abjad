from abjad import *
import py.test


def test_Note___setattr___01( ):
   '''Slots constrain note attributes.
   '''

   note = Note(0, (1, 4))

   assert py.test.raises(AttributeError, "note.foo = 'bar'")
