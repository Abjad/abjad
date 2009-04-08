from abjad import *


def test_parentage_parentage_01( ):
   '''t.parentage.parentage return a list of the elements
      in the parentage of leaf t, including t.'''

   t = Score([Staff(Container(run(2)) * 2)])
   pitches.diatonicize(t)

   r'''\new Score <<
      \new Staff {
         {
            c'8
            d'8
         }
         {
            e'8
            f'8
         }
      }
   >>'''

   parentage = t.leaves[0].parentage.parentage

   "[Note(c', 8), Container(c'8, d'8), Staff{2}, Score<<1>>]"

   assert len(parentage) == 4
   assert parentage[0] is t[0][0][0]
   assert parentage[1] is t[0][0]
   assert parentage[2] is t[0]
   assert parentage[3] is t


def test_parentage_parentage_02( ):
   '''t.parentage.parentage returns a list of the elements
      in the parentage of container t, including t.'''

   t = Score([Staff(Container(run(2)) * 2)])
   pitches.diatonicize(t)

   r'''\new Score <<
      \new Staff {
         {
            c'8
            d'8
         }
         {
            e'8
            f'8
         }
      }
   >>'''

   parentage = t[0][0].parentage.parentage

   "[Container(c'8, d'8), Staff{2}, Score<<1>>]"

   assert len(parentage) == 3
   assert parentage[0] is t[0][0]
   assert parentage[1] is t[0]
   assert parentage[2] is t
