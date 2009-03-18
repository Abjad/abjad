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
   '''True for orphan components when allow_orphans is True.
      False for orphan components when allow_orphans is False.'''

   t = scale(4)

   assert _are_strictly_contiguous_components_in_same_score(t)
   assert not _are_strictly_contiguous_components_in_same_score(
      t, allow_orphans = False)


def test_are_strictly_contiguous_components_in_same_score_04( ):
   '''Empty list returns True.'''

   t = [ ]

   assert _are_strictly_contiguous_components_in_same_score(t)
