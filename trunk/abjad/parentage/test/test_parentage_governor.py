from abjad import *


def test_parentage_governor_01( ):
   '''Return the last sequential container in the parentage of client
      such that the next element in the parentage of client is
      either a parallel container or None.'''

   t = Voice([Container(Voice(run(2)) * 2)])
   t[0].parallel = True
   diatonicize(t)
   t[0][0].name = 'voice 1'
   t[0][1].name = 'voice 2'

   r'''\new Voice {
      <<
         \context Voice = "voice 1" {
            c'8
            d'8
         }
         \context Voice = "voice 2" {
            e'8
            f'8
         }
      >>
   }'''

   assert t.leaves[0].parentage._governor is t[0][0]
   assert t.leaves[1].parentage._governor is t[0][0]
   assert t.leaves[2].parentage._governor is t[0][1]
   assert t.leaves[3].parentage._governor is t[0][1]


def test_parentage_governor_02( ):
   '''Unicorporated leaves have no governor.'''

   t = Note(0, (1, 8))
   assert t.parentage._governor is None


def test_parentage_governor_03( ):
   '''Return the last sequential container in the parentage of client
      such that the next element in the parentage of client is
      either a parallel container or None.'''

   t = Staff([Voice([Container(scale(4))])])

   r'''\new Staff {
      \new Voice {
         {
            c'8
            d'8
            e'8
            f'8
         }
      }
   }'''
   
   assert t.leaves[0].parentage._governor is t
   assert t.leaves[1].parentage._governor is t
   assert t.leaves[2].parentage._governor is t
   assert t.leaves[3].parentage._governor is t


def test_parentage_governor_04( ):
   '''Return the last sequential container in the parentage of client
      such that the next element in the parentage of client is
      either a parallel container or None.'''

   t = Staff([Voice([Container(scale(4))])])

   r'''\new Staff {
      \new Voice {
         {
            c'8
            d'8
            e'8
            f'8
         }
      }
   } '''

   assert t[0][0].parentage._governor is t
   assert t[0].parentage._governor is t
   assert t.parentage._governor is t
