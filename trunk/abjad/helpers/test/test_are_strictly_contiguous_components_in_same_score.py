from abjad.helpers.are_strictly_contiguous_components_in_same_score import _are_strictly_contiguous_components_in_same_score
from abjad import *


def test_are_strictly_contiguous_components_in_same_score_01( ):
   '''True for strictly contiguous leaves in voice.
      False for other time orderings of leaves in voice.'''

   t = Voice(scale(4))
   
   assert _are_strictly_contiguous_components_in_same_score(t.leaves)

   assert not _are_strictly_contiguous_components_in_same_score(
      list(reversed(t.leaves)))
   assert not _are_strictly_contiguous_components_in_same_score(
      t.leaves[2:] + t.leaves[:2])
   assert not _are_strictly_contiguous_components_in_same_score(
      t[3:4] + t[0:1])
   assert not _are_strictly_contiguous_components_in_same_score(
      [t] + t.leaves)


def test_are_strictly_contiguous_components_in_same_score_02( ):
   '''True for unincorporated components.
      True across container boundaries.'''

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

   assert _are_strictly_contiguous_components_in_same_score([t])
   assert _are_strictly_contiguous_components_in_same_score(t[:])
   assert _are_strictly_contiguous_components_in_same_score(t[0][:])
   assert _are_strictly_contiguous_components_in_same_score(t[1][:])
   assert _are_strictly_contiguous_components_in_same_score(t.leaves)


def test_are_strictly_contiguous_components_in_same_score_03( ):
   '''False for more than one unincorporated component.'''

   t = scale(4)

   assert not _are_strictly_contiguous_components_in_same_score(t)


def test_are_strictly_contiguous_components_in_same_score_04( ):
   '''Empty list returns True.'''

   t = [ ]

   assert _are_strictly_contiguous_components_in_same_score(t)
