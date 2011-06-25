from abjad import *
import py.test


def test__LeafDurationInterface___slots___01( ):
   '''Slots contstrain leaf duration interface attributes.
   '''

   note = Note("c'4")

   assert py.test.raises(AttributeError, "note.duration.foo = 'bar'")
