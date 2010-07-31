from abjad import *


def test_Component__ID_01( ):
   '''Return component name if it exists, otherwise Python ID.'''

   t = Staff(macros.scale(4))
   assert t._ID.startswith('Staff-')


def test_Component__ID_02( ):
   '''Return component name if it exists, otherwise Python ID.'''

   t = Staff(macros.scale(4))
   t.name = 'foo'
   assert t._ID == 'Staff-foo'
