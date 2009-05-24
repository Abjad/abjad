from abjad import *


def test_spacing_interface_grob_handling_01( ):
   '''Handle *LilyPond* ``SpacingSpanner`` grob on ``Score``.
      Note that it doesn't make much sense to override the *LilyPond*
      ``SpacingSpanner`` at ``Note``, ``Voice`` or ``Staff``.'''

   t = Score([ ])
   t.spacing.strict_grace_spacing = True
   t.spacing.strict_note_spacing = True
   t.spacing.uniform_stretching = True

   r'''\new Score \with {
           \override SpacingSpanner #'strict-note-spacing = ##t
           \override SpacingSpanner #'uniform-stretching = ##t
           \override SpacingSpanner #'strict-grace-spacing = ##t
   } <<
   >>'''

   assert check.wf(t)
   assert t.format == "\\new Score \\with {\n\t\\override SpacingSpanner #'strict-note-spacing = ##t\n\t\\override SpacingSpanner #'uniform-stretching = ##t\n\t\\override SpacingSpanner #'strict-grace-spacing = ##t\n} <<\n>>"
