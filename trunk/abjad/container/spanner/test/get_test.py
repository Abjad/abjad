from abjad import *


def test_get_01( ):
   '''
   Get spanners spanning leaves in container by classname.
   '''

   t = Voice(run(5))
   appictate(t)
   Beam(t[0 : 2])
   Beam(t[3 : 5])

   r'''
   \new Voice {
      c'8 [
      cs'8 ]
      d'8
      ef'8 [
      e'8 ]
   }
   '''

   spanners = t.spanners.get(classname = 'Beam')
   assert len(spanners) == 2
   assert spanners[0][0] is t[0]
   assert spanners[0][1] is t[1]
   assert spanners[1][0] is t[3]
   assert spanners[1][1] is t[4]
