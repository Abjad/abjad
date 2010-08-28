from abjad import *


def test_SpacingSpanner_new_section_01( ):
   r'''Apply LilyPond spacing section to Abjad leaves.'''

   t = Staff(macros.scale(4))
   #p = spannertools.SpacingSpanner(t[:])
   #p.new_section = True
   marktools.LilyPondCommandMark('new_spacing_section')(t[0])


   r'''
   \new Staff {
           \newSpacingSection
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t\\newSpacingSection\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_SpacingSpanner_new_section_02( ):
   '''Apply LilyPond spacing section to Abjad measures.'''

   t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
   #p = spannertools.SpacingSpanner(t[:])
   #p.new_section = True
   marktools.LilyPondCommandMark('new_spacing_section')(t[0])

   r'''
   \new Staff {
           {
                   \newSpacingSection
                   \time 2/8
                   c'8
                   c'8
           }
           {
                   \time 2/8
                   c'8
                   c'8
           }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\newSpacingSection\n\t\t\\time 2/8\n\t\tc'8\n\t\tc'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\tc'8\n\t}\n}"
