from abjad import *
import py.test


def test__OffsetInterface___slots___01( ):
   '''Slots constraint offset interface attributes.
   '''

   note = Note(0, (1, 4))
   
   assert py.test.raises(AttributeError, "note._offset.foo = 'bar'")
