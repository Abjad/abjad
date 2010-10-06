from abjad import *
import py.test


def test_NoteHead___slots___01( ):
   '''Slots constrain note head attributes.
   '''
   
   note_head = notetools.NoteHead("cs''")

   assert py.test.raises(AttributeError, "note_head.foo = 'bar'")
