from abjad import *


def test_SpacingInterface_grob_handling_01( ):
   '''Handle LilyPond ``SpacingSpanner`` grob on ``Score``.
   Note that it doesn't make much sense to override the LilyPond
   ``SpacingSpanner`` at ``Note``, ``Voice`` or ``Staff``.
   '''

   t = Score([ ])
   t.override.spacing_spanner.strict_grace_spacing = True
   t.override.spacing_spanner.strict_note_spacing = True
   t.override.spacing_spanner.uniform_stretching = True

   r'''
   \new Score \with {
      \override SpacingSpanner #'strict-grace-spacing = ##t
      \override SpacingSpanner #'strict-note-spacing = ##t
      \override SpacingSpanner #'uniform-stretching = ##t
   } <<
   >>
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Score \\with {\n\t\\override SpacingSpanner #'strict-grace-spacing = ##t\n\t\\override SpacingSpanner #'strict-note-spacing = ##t\n\t\\override SpacingSpanner #'uniform-stretching = ##t\n} <<\n>>"
