from abjad.component.component import _Component
from abjad import *
import py.test


def test_assess_components_none_parent_01( ):
   
   t = Voice(Container(run(2)) * 2)
   pitches.diatonicize(t)

   r'''\new Voice {
      {
         c'8
         d'8
      }
      {
         e'8
         f'8
      }
   }'''

   
   assert assess_components(t[:], share = 'parent')
   assert assess_components(t.leaves[:2], share = 'parent')
   assert assess_components(t.leaves[2:], share = 'parent')

   assert assess_components([t], share = 'parent')
   assert not assess_components([t], share = 'parent', allow_orphans = False)

   assert not assess_components(t.leaves, share = 'parent')
   assert not assess_components(list(iterate(t, _Component)), share = 'parent')


def test_assess_components_none_parent_02( ):

   t1 = Voice(scale(4))
   t2 = Voice(scale(4))

   assert assess_components(t1.leaves, share = 'parent')
   assert assess_components(t2.leaves, share = 'parent')

   assert assess_components([t1], share = 'parent')
   assert not assess_components([t1], share = 'parent', allow_orphans = False)

   assert assess_components([t2], share = 'parent')
   assert not assess_components([t2], share = 'parent', allow_orphans = False)

   assert assess_components([t1, t2], share = 'parent')
   assert not assess_components([t1, t2], share = 'parent', 
      allow_orphans = False)

   assert not assess_components(t1.leaves + t2.leaves, share = 'parent')


def test_assess_components_none_parent_03( ):
   '''Nonlist input raises TypeError.'''

   assert py.test.raises(TypeError, 
      'assess_components(Note(0, (1, 8)))', share = 'parent')


def test_assess_components_none_parent_04( ):
   '''Empty list returns True.'''

   assert assess_components([ ], share = 'parent')
