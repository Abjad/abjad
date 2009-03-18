from abjad.component.component import _Component
from abjad.helpers.are_components_in_same_parent import _are_components_in_same_parent
from abjad import *
import py.test


def test_are_components_in_same_parent_01( ):
   
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

   
   assert _are_components_in_same_parent(t[:])
   assert _are_components_in_same_parent(t.leaves[:2])
   assert _are_components_in_same_parent(t.leaves[2:])

   assert _are_components_in_same_parent([t])
   assert not _are_components_in_same_parent([t], allow_orphans = False)

   assert not _are_components_in_same_parent(t.leaves)
   assert not _are_components_in_same_parent(list(iterate(t, _Component)))


def test_are_components_in_same_parent_02( ):

   t1 = Voice(scale(4))
   t2 = Voice(scale(4))

   assert _are_components_in_same_parent(t1.leaves)
   assert _are_components_in_same_parent(t2.leaves)

   assert _are_components_in_same_parent([t1])
   assert not _are_components_in_same_parent([t1], allow_orphans = False)

   assert _are_components_in_same_parent([t2])
   assert not _are_components_in_same_parent([t2], allow_orphans = False)

   assert _are_components_in_same_parent([t1, t2])
   assert not _are_components_in_same_parent([t1, t2], allow_orphans = False)

   assert not _are_components_in_same_parent(t1.leaves + t2.leaves)


def test_are_components_in_same_parent_03( ):
   '''Nonlist input raises TypeError.'''

   assert py.test.raises(TypeError, 
      '_are_components_in_same_parent(Note(0, (1, 8)))')


def test_are_components_in_same_parent_04( ):
   '''Empty list returns True.'''

   assert _are_components_in_same_parent([ ])
