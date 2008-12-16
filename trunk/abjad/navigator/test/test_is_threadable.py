from abjad import *
import py.test


py.test.skip('Maybe we should replace _isThreadable with _pathExistsBetween.')

### TODO - I think the current implementation of _isThreadable
###        is mismodelling a couple of small things.
###        The tests in this file give minimal examples so we
###        can determine and then enforce the best behavior.

### THIS TEST IS OK ###
def test_is_threadable_01( ):
   r'''Threading leaves across non-\new and 
       non-\context boundaries works fine;
       this is true in the current implementation
       and should remain so..'''

   s1 = Sequential([Note(i, (1, 8)) for i in range(4)])
   s2 = Sequential([Note(i, (1, 8)) for i in range(4, 8)])
   seq = Sequential([s1, s2])

   assert seq[0][-1]._navigator._isThreadable(seq[1][0])
   assert seq[1][0]._navigator._isThreadable(seq[0][-1])

   r'''
   {
      {
         c'8
         cs'8
         d'8
         ef'8
      }
      {
         e'8
         f'8
         fs'8
         g'8
      }
   }
   '''

   
def test_is_threadable_02( ):
   r'''The current implementation allows threading across
      the two different \new boundaries between separating
      the last note of the first (anonymous) voice and first
      note of the second (anonymous) voice.

      LilyPond will complain of, for example, unterminated
      beams that begin in the first voice and 'end' in the second.

      This should change and we should block threading here.'''

   v1 = Voice([Note(i, (1, 8)) for i in range(4)])
   v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   seq = Sequential([v1, v2])

   assert not seq[0][-1]._navigator._isThreadable(seq[1][0])
   assert not seq[1][0]._navigator._isThreadable(seq[0][-1])


def test_is_threadable_03( ):
   r'''The current implementation allows threading from
       the last note of the first voice up across the \new
       boundary of the first voice, up across the \new boundary
       of the first staff, over across the \new boundary of
       the second staff, and down across the \new boundary of
       the second voice.

       Moving from the last note of the first voice to the first
       note of the second voice crosses over four different
       \new boundaries.

       Additionally, moving from the first voice to the second
       voice also crosses over four different \new boundaries.

       And last, moving from the first staff to the second
       staff crosses over two different \new boundaries.

       LilyPond will complain of, for example, unterminated
       beams that begin in the first voice and 'end' in the second.

       This should change and we should block threading here.'''

   v1 = Voice([Note(i, (1, 8)) for i in range(4)])
   v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   s1 = Staff([v1])
   s2 = Staff([v2])
   seq = Sequential([s1, s2])
   
   ### notes shouldn't thread ###
   assert not seq[0][0][-1]._navigator._isThreadable(seq[1][0][0])
   assert not seq[1][0][0]._navigator._isThreadable(seq[0][0][-1])

   ### voices shouldn't thread ###
   assert not seq[0][0]._navigator._isThreadable(seq[1][0])
   assert not seq[1][0]._navigator._isThreadable(seq[0][0])

   ### staves shouldn't thread ###
   assert not seq[0]._navigator._isThreadable(seq[1])
   assert not seq[0]._navigator._isThreadable(seq[0])

   r'''
   {
      \new Staff {
         \new Voice {
            c'8
            cs'8
            d'8
            ef'8
         }
      }
      \new Staff {
         \new Voice {
            e'8
            f'8
            fs'8
            g'8
         }
      }
   }
   '''
