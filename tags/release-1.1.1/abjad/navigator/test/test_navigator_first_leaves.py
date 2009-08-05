from abjad import *
import py.test


def test_navigator_first_leaves_01( ):
   '''Return first leaf from sequential container.'''

   t = Voice(construct.scale(4))
   leaves = t._navigator._firstLeaves

   assert len(leaves) == 1
   assert leaves[0] is t[0]


def test_navigator_first_leaves_02( ):
   '''Return first leaves from parallel containers.'''

   t = Container(Voice(construct.run(2)) * 2)
   t.parallel = True
   pitchtools.diatonicize(t)
   leaves = t._navigator._firstLeaves

   r'''<<
      \new Voice {
         c'8
         d'8
      }
      \new Voice {
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

   t = Container(Voice([ ]) * 2)
   t.parallel = True
   leaves = t._navigator._firstLeaves
   assert len(leaves) == 0
