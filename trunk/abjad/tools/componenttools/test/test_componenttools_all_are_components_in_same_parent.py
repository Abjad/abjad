from abjad.component.component import _Component
from abjad import *
import py.test


def test_componenttools_all_are_components_in_same_parent_01( ):
   
   t = Voice(Container(leaftools.make_repeated_notes(2)) * 2)
   pitchtools.diatonicize(t)

   r'''
   \new Voice {
      {
         c'8
         d'8
      }
      {
         e'8
         f'8
      }
   }
   '''

   
   assert componenttools.all_are_components_in_same_parent(t[:])
   assert componenttools.all_are_components_in_same_parent(t.leaves[:2])
   assert componenttools.all_are_components_in_same_parent(t.leaves[2:])

   assert componenttools.all_are_components_in_same_parent([t])
   assert not componenttools.all_are_components_in_same_parent([t], allow_orphans = False)

   assert not componenttools.all_are_components_in_same_parent(t.leaves)
   assert not componenttools.all_are_components_in_same_parent(
      list(iterate.naive_forward_in_expr(t, _Component)))


def test_componenttools_all_are_components_in_same_parent_02( ):

   t1 = Voice(macros.scale(4))
   t2 = Voice(macros.scale(4))

   assert componenttools.all_are_components_in_same_parent(t1.leaves)
   assert componenttools.all_are_components_in_same_parent(t2.leaves)

   assert componenttools.all_are_components_in_same_parent([t1])
   assert not componenttools.all_are_components_in_same_parent([t1], allow_orphans = False)

   assert componenttools.all_are_components_in_same_parent([t2])
   assert not componenttools.all_are_components_in_same_parent([t2], allow_orphans = False)

   assert componenttools.all_are_components_in_same_parent([t1, t2])
   assert not componenttools.all_are_components_in_same_parent([t1, t2], 
      allow_orphans = False)

   assert not componenttools.all_are_components_in_same_parent(t1.leaves + t2.leaves)


def test_componenttools_all_are_components_in_same_parent_03( ):
   '''Nonlist input raises TypeError.'''

   assert py.test.raises(TypeError, 
      'componenttools.all_are_components_in_same_parent(Note(0, (1, 8)))')


def test_componenttools_all_are_components_in_same_parent_04( ):
   '''Empty list returns True.'''

   assert componenttools.all_are_components_in_same_parent([ ])
