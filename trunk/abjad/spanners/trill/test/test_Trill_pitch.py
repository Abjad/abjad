from abjad import *


def test_Trill_pitch_01( ):
   '''Assign Abjad pitch instance to create a pitched trill.'''

   t = Staff(macros.scale(4))
   trill = Trill(t[:2])
   trill.pitch = Pitch(1)

   r'''
   \new Staff {
      \pitchedTrill c'8 \startTrillSpan cs'
      d'8 \stopTrillSpan
      e'8
      f'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t\\pitchedTrill c'8 \\startTrillSpan cs'\n\td'8 \\stopTrillSpan\n\te'8\n\tf'8\n}"


def test_Trill_pitch_02( ):
   '''Any pitch init value will work.'''

   t = Staff(macros.scale(4))
   trill = Trill(t[:2])
   trill.pitch = 1

   r'''
   \new Staff {
      \pitchedTrill c'8 \startTrillSpan cs'
      d'8 \stopTrillSpan
      e'8
      f'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t\\pitchedTrill c'8 \\startTrillSpan cs'\n\td'8 \\stopTrillSpan\n\te'8\n\tf'8\n}"


def test_Trill_pitch_03( ):
   '''Clear with None.'''

   t = Staff(macros.scale(4))
   trill = Trill(t[:2])
   trill.pitch = Pitch(1)
   trill.pitch = None

   r'''
   \new Staff {
      c'8 \startTrillSpan
      d'8 \stopTrillSpan
      e'8
      f'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\tc'8 \\startTrillSpan\n\td'8 \\stopTrillSpan\n\te'8\n\tf'8\n}"
