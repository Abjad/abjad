from abjad.component.component import _Component
from abjad.helpers.test_components import _test_components
from abjad import *
import py.test


def test_test_components_none_parent_01( ):
   
   t = Voice(Sequential(run(2)) * 2)
   diatonicize(t)

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

   
   assert _test_components(t[:], share = 'parent')
   assert _test_components(t.leaves[:2], share = 'parent')
   assert _test_components(t.leaves[2:], share = 'parent')

   assert _test_components([t], share = 'parent')
   assert not _test_components([t], share = 'parent', allow_orphans = False)

   assert not _test_components(t.leaves, share = 'parent')
   assert not _test_components(list(iterate(t, _Component)), share = 'parent')


def test_test_components_none_parent_02( ):

   t1 = Voice(scale(4))
   t2 = Voice(scale(4))

   assert _test_components(t1.leaves, share = 'parent')
   assert _test_components(t2.leaves, share = 'parent')

   assert _test_components([t1], share = 'parent')
   assert not _test_components([t1], share = 'parent', allow_orphans = False)

   assert _test_components([t2], share = 'parent')
   assert not _test_components([t2], share = 'parent', allow_orphans = False)

   assert _test_components([t1, t2], share = 'parent')
   assert not _test_components([t1, t2], share = 'parent', 
      allow_orphans = False)

   assert not _test_components(t1.leaves + t2.leaves, share = 'parent')


def test_test_components_none_parent_03( ):
   '''Nonlist input raises TypeError.'''

   assert py.test.raises(TypeError, 
      '_test_components(Note(0, (1, 8)))', share = 'parent')


def test_test_components_none_parent_04( ):
   '''Empty list returns True.'''

   assert _test_components([ ], share = 'parent')
