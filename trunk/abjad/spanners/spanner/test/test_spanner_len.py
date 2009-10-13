from abjad import *


def test_spanner_len_01( ):
   '''Spanner length equals length of components.'''

   t = Voice(Container(construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   p = Beam(t[1])

   r'''\new Voice {
      {
         c'8
         d'8
      }
      {
         e'8 [
         f'8 ]
      }
      {
         g'8
         a'8
      }
   }'''

   assert len(p) == 1
   assert len(p.components) == 1
   assert len(p.leaves) == 2


def test_spanner_len_02( ):
   '''Spanner length equals length of components.'''

   t = Voice(Container(construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   p = Beam(t[:])

   r'''\new Voice {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8
      }
      {
         g'8
         a'8 ]
      }
   }'''

   assert len(p) == 3
   assert len(p.components) == 3
   assert len(p.leaves) == 6
