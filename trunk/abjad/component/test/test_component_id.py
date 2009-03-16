from abjad import *


def test_component_id_01( ):
   '''Return invocation name if it exists, otherwise Python ID.'''

   t = Staff(scale(4))
   assert t._ID.startswith('Staff-')


def test_component_id_02( ):
   '''Return invocation name if it exists, otherwise Python ID.'''

   t = Staff(scale(4))
   t.invocation.name = 'foo'
   assert t._ID == 'Staff-foo'
