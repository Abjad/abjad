from abjad import *


def test_context_id_01( ):
   '''Return invocation name if it exists, otherwise Python ID.'''

   t = Staff(scale(4))
   assert isinstance(t._ID, int)


def test_context_id_02( ):
   '''Return invocation name if it exists, otherwise Python ID.'''

   t = Staff(scale(4))
   t.invocation.name = 'foo'
   assert t._ID == 'foo'
