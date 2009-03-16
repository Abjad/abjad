from abjad import *
import py.test


def test_is_threadable_01( ):
   r'''Threading leaves across non-\new and 
      non-\context boundaries works fine.'''

   t = Sequential(Sequential(run(4)) * 2)
   appictate(t)

   assert t[0][-1]._navigator._isThreadable(t[1][0])
   assert t[1][0]._navigator._isThreadable(t[0][-1])

   r'''{
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
   }'''

   
def test_is_threadable_02( ):
   r'''LilyPond DOES NOT allow threading across different anonymous voices.
      _isThreadable( ) DOES allows threading across anonymous voices.'''

   t = Sequential(Voice(run(4)) * 2)
   appictate(t)

   ## TODO - make these asserts work

   assert not t[0][-1]._navigator._isThreadable(t[1][0])
   assert not t[1][0]._navigator._isThreadable(t[0][-1])

   r'''{
      \new Voice {
         c'8
         cs'8
         d'8
         ef'8
      }
      \new Voice {
         e'8
         f'8
         fs'8
         g'8
      }
   }'''


def test_is_threadable_03( ):
   r'''LilyPond forbids threading across anonymous staves.
      LilyPond forbids threading across anonymous voices.
      _isThreadable( ) allows threading across anonymous staves.
      _isThreadable( ) allows threading across anonymous voices.''' 

   t = Sequential(Staff([Voice(run(4))]) * 2)
   appictate(t)
   
   ## TODO - make these asserts work

   assert not t[0][0][-1]._navigator._isThreadable(t[1][0][0])
   assert not t[1][0][0]._navigator._isThreadable(t[0][0][-1])

   assert not t[0][0]._navigator._isThreadable(t[1][0])
   assert not t[1][0]._navigator._isThreadable(t[0][0])

   assert not t[0]._navigator._isThreadable(t[1])
   assert t[0]._navigator._isThreadable(t[0])

   r'''{
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
   }'''
