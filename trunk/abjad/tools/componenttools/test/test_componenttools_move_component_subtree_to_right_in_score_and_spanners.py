from abjad import *


def test_componenttools_move_component_subtree_to_right_in_score_and_spanners_01( ):
   '''Flip leaf under continuous spanner.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   Beam(t[:])

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   componenttools.move_component_subtree_to_right_in_score_and_spanners(t[1])

   r'''
   \new Voice {
      c'8 [
      e'8
      d'8
      f'8 ]
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\te'8\n\td'8\n\tf'8 ]\n}"


def test_componenttools_move_component_subtree_to_right_in_score_and_spanners_02( ):
   '''Flip leaf across spanner boundaries.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   Beam(t[:2])
   Beam(t[2:])

   r'''
   \new Voice {
      c'8 [
      d'8 ]
      e'8 [
      f'8 ]
   }
   '''

   componenttools.move_component_subtree_to_right_in_score_and_spanners(t[1])
   
   r'''
   \new Voice {
      c'8 [
      e'8 ]
      d'8 [
      f'8 ]
   }
   '''
   
   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\te'8 ]\n\td'8 [\n\tf'8 ]\n}"


def test_componenttools_move_component_subtree_to_right_in_score_and_spanners_03( ):
   '''Flip leaf from within to without spanner.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   Beam(t[:2])

   r'''
   \new Voice {
      c'8 [
      d'8 ]
      e'8
      f'8
   }
   '''

   componenttools.move_component_subtree_to_right_in_score_and_spanners(t[1])

   r'''
   \new Voice {
      c'8 [
      e'8 ]
      d'8
      f'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\te'8 ]\n\td'8\n\tf'8\n}"
