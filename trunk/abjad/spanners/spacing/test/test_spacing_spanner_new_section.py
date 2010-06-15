from abjad import *


def test_spacing_spanner_new_section_01( ):
   r'''Apply LilyPond spacing section to Abjad leaves.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   p = SpacingSpanner(t[:])
   p.new_section = True

   r'''
   \new Staff {
           \newSpacingSection
           c'8
           d'8
           e'8
           f'8
           %%% spacing section ends here %%%
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t\\newSpacingSection\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t%%% spacing section ends here %%%\n}"


def test_spacing_spanner_new_section_02( ):
   '''Apply LilyPond spacing section to Abjad measures.'''

   t = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 2)
   p = SpacingSpanner(t[:])
   p.new_section = True

   r'''
   \new Staff {
           {
                   \time 2/8
                   \newSpacingSection
                   c'8
                   c'8
           }
           {
                   \time 2/8
                   c'8
                   c'8
                   %%% spacing section ends here %%%
           }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\t\\newSpacingSection\n\t\tc'8\n\t\tc'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\tc'8\n\t\t%%% spacing section ends here %%%\n\t}\n}"
