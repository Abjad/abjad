from abjad import *


def test_Spanner___init____01( ):
   '''Init empty spanner.'''

   p = BeamSpanner( )
   assert len(p) == 0
   assert p[:] == [ ]


def test_Spanner___init____02( ):
   '''Init nonempty spanner.'''

   t = Container(macros.scale(4))
   p = BeamSpanner(t[:])

   r'''
   {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   assert len(p) == 4
   assert p[:] == t[:]
