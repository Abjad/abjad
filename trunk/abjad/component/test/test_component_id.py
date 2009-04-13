from abjad import *


def test_component_id_01( ):
   '''Return component name if it exists, otherwise Python ID.'''

   t = Staff(construct.scale(4))
   assert t._ID.startswith('Staff-')


def test_component_id_02( ):
   '''Return component name if it exists, otherwise Python ID.'''

   t = Staff(construct.scale(4))
   t.name = 'foo'
   assert t._ID == 'Staff-foo'
