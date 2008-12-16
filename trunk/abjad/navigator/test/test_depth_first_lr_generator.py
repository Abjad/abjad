from abjad import *
import py.test


def test_depth_first_lr_generator_01( ):
   '''Results.'''

   s1 = Sequential([Note(n, (1, 8)) for n in range(4)])
   notes = [Note(n, (1, 8)) for n in range(4, 8)]
   t = Voice([s1] + notes)
   g = t._navigator._depthFirstLeftToRight( )

   assert g.next( ) is t
   assert g.next( ) is t[0]
   assert g.next( ) is t[0][0]
   assert g.next( ) is t[0]
   assert g.next( ) is t[0][1]
   assert g.next( ) is t[0]
   assert g.next( ) is t[0][2]
   assert g.next( ) is t[0]
   assert g.next( ) is t[0][3]
   assert g.next( ) is t[0]
   assert g.next( ) is t
   assert g.next( ) is t[1]
   assert g.next( ) is t
   assert g.next( ) is t[2]
   assert g.next( ) is t
   assert g.next( ) is t[3]
   assert g.next( ) is t
   assert g.next( ) is t[4]
   assert g.next( ) is t
   assert py.test.raises(StopIteration, 'g.next( )')

   r'''
   \new Voice {
      {
         c'8
         cs'8
         d'8
         ef'8
      }
      e'8
      f'8
      fs'8
      g'8
   }
   '''


def test_depth_first_lr_generator_02( ):
   '''Results.'''

   notes = [Note(n, (1, 8)) for n in range(4)]
   s1 = Sequential([Note(n, (1, 8)) for n in range(4, 8)])
   t = Voice(notes + [s1])
   g = t._navigator._depthFirstLeftToRight( )

   assert g.next( ) is t
   assert g.next( ) is t[0]
   assert g.next( ) is t
   assert g.next( ) is t[1]
   assert g.next( ) is t
   assert g.next( ) is t[2]
   assert g.next( ) is t
   assert g.next( ) is t[3]
   assert g.next( ) is t
   assert g.next( ) is t[4]
   assert g.next( ) is t[4][0]
   assert g.next( ) is t[4]
   assert g.next( ) is t[4][1]
   assert g.next( ) is t[4]
   assert g.next( ) is t[4][2]
   assert g.next( ) is t[4]
   assert g.next( ) is t[4][3]
   assert g.next( ) is t[4]
   assert g.next( ) is t
   assert py.test.raises(StopIteration, 'g.next( )')

   r'''
   \new Voice {
      c'8
      cs'8
      d'8
      ef'8
      {
         e'8
         f'8
         fs'8
         g'8
      }
   }
   '''
