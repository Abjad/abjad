from abjad import *


def test_container_clear_01( ):
   '''
   Containers clear unspanned child leaves.
   '''

   t = Staff(scale(4))
   contents = t[ : ]
   result = t.clear( )

   r'''
   \new Staff {
   }
   '''

   assert t.format == '\\new Staff {\n}'
   assert len(t) == 0

   "[Note(c', 8), Note(d', 8), Note(e', 8), Note(f', 8)]"

   assert contents == result
   assert len(result) == 4

   for x in result:
      assert x.parentage.parent is None


def test_container_clear_02( ):
   '''
   Containers clear spanned child leaves.
   '''

   t = Staff(scale(4))
   p = Beam(t[ : ])
   contents = t[ : ]
   result = t.clear( )

   r'''
   \new Staff {
   }
   '''

   assert t.format == '\\new Staff {\n}'
   assert len(t) == 0

   "[Note(c', 8), Note(d', 8), Note(e', 8), Note(f', 8)]"

   '''
   c'8 [
   d'8
   e'8
   f'8 ]
   '''

   assert contents == result
   assert len(result) == 4

   for x in result:
      assert x.parentage.parent is None
      assert x.beam.spanned

  
def test_container_clear_03( ):
   '''
   Containers clear unspanned child containers.
   '''

   t = Staff(Sequential(run(2)) * 3)
   diatonicize(t)
   contents = t[ : ]

   r'''
   \new Staff {
      {
         c'8
         d'8
      }
      {
         e'8
         f'8
      }
      {
         g'8
         a'8
      }
   }
   '''

   result = t.clear( )
   assert len(t) == 0
   assert len(result) == 3

   '''
   {
      c'8
      d'8
   }
   {
      e'8
      f'8
   }
   {
      g'8
      a'8
   }
   '''

   assert result == contents
   for x in result:
      assert x.parentage.parent is None


def test_container_clear_04( ):
   '''
   Containers clear spanned child containers.
   '''

   t = Staff(Sequential(run(2)) * 3)
   p = Beam(t[ : ])
   diatonicize(t)
   contents = t[ : ]

   r'''
   \new Staff {
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
   }
   '''

   result = t.clear( )
   assert len(t) == 0
   assert len(result) == 3

   '''
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
   '''

   assert result == contents
   for x in result:
      assert x.parentage.parent is None
      assert x.beam.spanned
