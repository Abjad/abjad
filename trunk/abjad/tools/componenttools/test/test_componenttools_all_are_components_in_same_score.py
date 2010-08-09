from abjad.components._Component._Component import _Component
from abjad import *


def test_componenttools_all_are_components_in_same_score_01( ):
   '''All components here in the same score.'''
   
   t = Voice(Container(leaftools.make_repeated_notes(2)) * 2)
   pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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

   assert componenttools.all_are_components_in_same_score([t])
   assert componenttools.all_are_components_in_same_score(t[:])
   assert componenttools.all_are_components_in_same_score(t.leaves[:2])
   assert componenttools.all_are_components_in_same_score(t.leaves[2:])
   assert componenttools.all_are_components_in_same_score(t.leaves)
   assert componenttools.all_are_components_in_same_score(
      list(iterate.naive_forward_in_expr(t, _Component)))


def test_componenttools_all_are_components_in_same_score_02( ):
   '''Components here divide between two different scores.'''

   t1 = Voice(macros.scale(4))
   t2 = Voice(macros.scale(4))

   assert componenttools.all_are_components_in_same_score([t1])
   assert componenttools.all_are_components_in_same_score(t1.leaves)
   assert componenttools.all_are_components_in_same_score([t2])
   assert componenttools.all_are_components_in_same_score(t2.leaves)

   assert componenttools.all_are_components_in_same_score([t1, t2])
   assert not componenttools.all_are_components_in_same_score([t1, t2], allow_orphans = False)

   assert not componenttools.all_are_components_in_same_score(t1.leaves + t2.leaves)


def test_componenttools_all_are_components_in_same_score_03( ):
   '''Unincorporated component returns True.'''

   assert componenttools.all_are_components_in_same_score([Note(0, (1, 8))])


def test_componenttools_all_are_components_in_same_score_04( ):
   '''Empty list returns True.'''

   assert componenttools.all_are_components_in_same_score([ ])
