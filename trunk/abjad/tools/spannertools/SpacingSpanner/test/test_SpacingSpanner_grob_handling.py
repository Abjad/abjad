from abjad import *


def test_SpacingSpanner_grob_handling_01( ):
   '''Override LilyPond SpacingSpanner grob on Abjad leaves.
   LilyPond SpacingSpanner lives at Score by default.
   Abjad SpacingSpanner overrides usually 
   require context promotion.
   '''

   t = Staff(macros.scale(4))
   p = spannertools.SpacingSpanner(t[:])
   p.override.score.spacing_spanner.strict_grace_spacing = True
   p.override.score.spacing_spanner.strict_note_spacing = True
   p.override.score.spacing_spanner.uniform_stretching = True

   r'''
   \new Staff {
      \override Score.SpacingSpanner #'strict-grace-spacing = ##t
      \override Score.SpacingSpanner #'strict-note-spacing = ##t
      \override Score.SpacingSpanner #'uniform-stretching = ##t
      c'8
      d'8
      e'8
      f'8
      \revert Score.SpacingSpanner #'strict-grace-spacing
      \revert Score.SpacingSpanner #'strict-note-spacing
      \revert Score.SpacingSpanner #'uniform-stretching
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t\\override Score.SpacingSpanner #'strict-grace-spacing = ##t\n\t\\override Score.SpacingSpanner #'strict-note-spacing = ##t\n\t\\override Score.SpacingSpanner #'uniform-stretching = ##t\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\revert Score.SpacingSpanner #'strict-grace-spacing\n\t\\revert Score.SpacingSpanner #'strict-note-spacing\n\t\\revert Score.SpacingSpanner #'uniform-stretching\n}"


def test_SpacingSpanner_grob_handling_02( ):
   '''Override LilyPond SpacingSpanner grob on Abjad containers.
   LilyPond SpacingSpanner lives at Score by default.
   Abjad SpacingSpanner overrides usually 
   require context promotion.
   '''

   t = Staff(RigidMeasure((2, 8), notetools.make_repeated_notes(2)) * 2)
   macros.diatonicize(t)
   p = spannertools.SpacingSpanner(t[:])
   p.override.score.spacing_spanner.strict_grace_spacing = True
   p.override.score.spacing_spanner.strict_note_spacing = True
   p.override.score.spacing_spanner.uniform_stretching = True
   

   r'''
   \new Staff {
           {
                   \time 2/8
                   \override Score.SpacingSpanner #'strict-grace-spacing = ##t
                   \override Score.SpacingSpanner #'strict-note-spacing = ##t
                   \override Score.SpacingSpanner #'uniform-stretching = ##t
                   c'8
                   d'8
           }
           {
                   \time 2/8
                   e'8
                   f'8
                   \revert Score.SpacingSpanner #'strict-note-spacing
                   \revert Score.SpacingSpanner #'strict-grace-spacing
                   \revert Score.SpacingSpanner #'uniform-stretching
           }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\t\\override Score.SpacingSpanner #'strict-grace-spacing = ##t\n\t\t\\override Score.SpacingSpanner #'strict-note-spacing = ##t\n\t\t\\override Score.SpacingSpanner #'uniform-stretching = ##t\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t\t\\revert Score.SpacingSpanner #'strict-grace-spacing\n\t\t\\revert Score.SpacingSpanner #'strict-note-spacing\n\t\t\\revert Score.SpacingSpanner #'uniform-stretching\n\t}\n}"
