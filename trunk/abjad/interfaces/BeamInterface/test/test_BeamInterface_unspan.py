from abjad import *


def test_BeamInterface_unspan_01( ):
   '''BeamInterface clone_components_and_remove_all_spanners( ) clears any beam spanner attaching to leaf t.'''

   t = Staff(macros.scale(4))
   p = spannertools.BeamSpanner(t[ : ])

   r'''
   \new Staff {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   #t[0].beam.unspan( )
   spannertools.destroy_all_spanners_attached_to_component(t[0], spannertools.BeamSpanner)

   r'''
   \new Staff {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"

   assert len(p) == 0
   #assert not t[0].beam.spanned
   #assert not t[1].beam.spanned
   #assert not t[2].beam.spanned
   #assert not t[3].beam.spanned
   assert not beamtools.is_component_with_beam_spanner_attached(t[0])
   assert not beamtools.is_component_with_beam_spanner_attached(t[1])
   assert not beamtools.is_component_with_beam_spanner_attached(t[2])
   assert not beamtools.is_component_with_beam_spanner_attached(t[3])


def test_BeamInterface_unspan_02( ):
   '''t.beam.unspan( ) clears any beam spanner attaching to container t.'''

   t = Staff(Container(notetools.make_repeated_notes(2)) * 2)
   macros.diatonicize(t)
   p = spannertools.BeamSpanner(t[ : ]) 

   r'''
   \new Staff {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8 ]
      }
   }
   '''
   
   #t[0].beam.unspan( )
   spannertools.destroy_all_spanners_attached_to_component(t[0], spannertools.BeamSpanner)

   r'''
   \new Staff {
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

   assert t.format == "\\new Staff {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n}"

   #assert not t[0].beam.spanned
   #assert not t[1].beam.spanned
   assert not beamtools.is_component_with_beam_spanner_attached(t[0])
   assert not beamtools.is_component_with_beam_spanner_attached(t[1])
   assert len(p) == 0
