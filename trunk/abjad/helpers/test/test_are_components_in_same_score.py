from abjad.component.component import _Component
from abjad.helpers.are_components_in_same_score import _are_components_in_same_score
from abjad import *


def test_are_components_in_same_score_01( ):
   '''All components here in the same score.'''
   
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

   
   assert _are_components_in_same_score([t])
   assert _are_components_in_same_score(t[:])
   assert _are_components_in_same_score(t.leaves[:2])
   assert _are_components_in_same_score(t.leaves[2:])
   assert _are_components_in_same_score(t.leaves)
   assert _are_components_in_same_score(list(iterate(t, _Component)))


def test_are_components_in_same_score_02( ):
   '''Components here divide between two different scores.'''

   t1 = Voice(scale(4))
   t2 = Voice(scale(4))

   assert _are_components_in_same_score([t1])
   assert _are_components_in_same_score(t1.leaves)
   assert _are_components_in_same_score([t2])
   assert _are_components_in_same_score(t2.leaves)

   assert _are_components_in_same_score([t1, t2])
   assert not _are_components_in_same_score([t1, t2], allow_orphans = False)

   assert not _are_components_in_same_score(t1.leaves + t2.leaves)


def test_are_components_in_same_score_03( ):
   '''Unincorporated component returns True.'''

   assert _are_components_in_same_score([Note(0, (1, 8))])


def test_are_components_in_same_score_04( ):
   '''Empty list returns True.'''

   assert _are_components_in_same_score([ ])
