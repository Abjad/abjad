from abjad.helpers.are_strictly_contiguous_components_in_same_parent import _are_strictly_contiguous_components_in_same_parent
from abjad import *


def test_are_strictly_contiguous_components_in_same_parent_01( ):
   '''True for strictly contiguous leaves in voice.
      False for other time orderings of leaves in voice.'''

   t = Voice(scale(4))
   
   assert _are_strictly_contiguous_components_in_same_parent(t.leaves)

   assert not _are_strictly_contiguous_components_in_same_parent(
      list(reversed(t.leaves)))
   assert not _are_strictly_contiguous_components_in_same_parent(
      t.leaves[2:] + t.leaves[:2])
   assert not _are_strictly_contiguous_components_in_same_parent(
      t[3:4] + t[0:1])
   assert not _are_strictly_contiguous_components_in_same_parent(
      [t] + t.leaves)


def test_are_strictly_contiguous_components_in_same_parent_02( ):
   '''False for unincorporated components.
      False across container boundaries.
      False for noncontiguous components.'''

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

   assert not _are_strictly_contiguous_components_in_same_parent([t])

   assert _are_strictly_contiguous_components_in_same_parent(t[:])

   assert _are_strictly_contiguous_components_in_same_parent(t[0][:])
   assert _are_strictly_contiguous_components_in_same_parent(t[1][:])

   assert not _are_strictly_contiguous_components_in_same_parent(t.leaves)


def test_are_strictly_contiguous_components_in_same_parent_03( ):
   '''Unicorporated leaves can not be evaluated for contiguity.'''

   t = scale(4)

   assert not _are_strictly_contiguous_components_in_same_parent(t)


def test_are_strictly_contiguous_components_in_same_parent_04( ):
   '''Empty list returns True.'''

   t = [ ]

   assert _are_strictly_contiguous_components_in_same_parent(t)
