from abjad import *
import py.test


def test_LeafDurationInterface___slots___01( ):
   '''Slots contstrain leaf duration interface attributes.
   '''

   note = Note(0, (1, 4))

   assert py.test.raises(AttributeError, "note.duration.foo = 'bar'")
