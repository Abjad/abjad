from abjad import *


def test_trill_spanner_pitch_01( ):
   '''Assign Abjad pitch instance to create a pitched trill.'''

   t = Staff(construct.scale(4))
   trill = Trill(t[:2])
   trill.pitch = Pitch(1)

   r'''\new Staff {
      \pitchedTrill c'8 \startTrillSpan cs'
      d'8 \stopTrillSpan
      e'8
      f'8
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\\pitchedTrill c'8 \\startTrillSpan cs'\n\td'8 \\stopTrillSpan\n\te'8\n\tf'8\n}"


def test_trill_spanner_pitch_02( ):
   '''Clear with None.'''

   t = Staff(construct.scale(4))
   trill = Trill(t[:2])
   trill.pitch = Pitch(1)
   trill.pitch = None

   r'''\new Staff {
      c'8 \startTrillSpan
      d'8 \stopTrillSpan
      e'8
      f'8
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'8 \\startTrillSpan\n\td'8 \\stopTrillSpan\n\te'8\n\tf'8\n}"
