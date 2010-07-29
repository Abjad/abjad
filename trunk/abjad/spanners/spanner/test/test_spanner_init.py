from abjad import *


def test_spanner_init_01( ):
   '''Init empty spanner.'''

   p = Beam( )
   assert len(p) == 0
   assert p[:] == [ ]


def test_spanner_init_02( ):
   '''Init nonempty spanner.'''

   t = Container(macros.scale(4))
   p = Beam(t[:])

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
