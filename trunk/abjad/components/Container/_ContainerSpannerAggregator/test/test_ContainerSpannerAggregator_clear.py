from abjad import *


def test_ContainerSpannerAggregator_clear_01( ):
   '''Clear one spanner attaching to container.'''

   t = Voice(Container(leaftools.make_repeated_notes(2)) * 3)
   pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
   p = Beam(t[:])

   r'''
   \new Voice {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8
      }
      {
         g'8
         a'8 ]
      }
   }
   '''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"

   t[0].spanners.clear( )

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
      {
         g'8
         a'8
      }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"


def test_ContainerSpannerAggregator_clear_02( ):
   '''Clear multiple spanners attaaching to container.'''

   t = Voice(Container(leaftools.make_repeated_notes(2)) * 3)
   pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
   p1 = Beam(t[:])
   p2 = Trill(t[ : ])
   
   r'''
   \new Voice {
      {
         c'8 [ \startTrillSpan
         d'8
      }
      {
         e'8
         f'8
      }
      {
         g'8
         a'8 ] \stopTrillSpan
      }
   } 
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\startTrillSpan\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ] \\stopTrillSpan\n\t}\n}"

   t[0].spanners.clear( )

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
      {
         g'8
         a'8
      }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"
