from abjad import *


def test_navigator_first_leaves_01( ):
   '''Return first leaf from sequential container.'''

   t = Voice(scale(4))
   leaves = t._navigator._firstLeaves

   assert len(leaves) == 1
   assert leaves[0] is t[0]


def test_navigator_first_leaves_02( ):
   '''Return first leaves from parallel containers.'''

   t = Parallel(Container(run(2)) * 2)
   diatonicize(t)
   leaves = t._navigator._firstLeaves

   r'''<<
      {
         c'8
         d'8
      }
      {
         e'8
         f'8
      }
   >>'''

   leaves = t._navigator._firstLeaves
   
   assert len(leaves) == 2
   assert leaves[0] is t[0][0]
   assert leaves[1] is t[1][0]


def test_navigator_first_leaves_03( ):
   '''Return first leaves from empty sequential container.'''

   t = Voice([ ])
   leaves = t._navigator._firstLeaves
   assert len(leaves) == 0


def test_navigator_first_leaves_04( ):
   '''Return first leaves from empty parallel containes.'''

   t = Parallel(Container([ ]) * 2)
   leaves = t._navigator._firstLeaves
   assert len(leaves) == 0
