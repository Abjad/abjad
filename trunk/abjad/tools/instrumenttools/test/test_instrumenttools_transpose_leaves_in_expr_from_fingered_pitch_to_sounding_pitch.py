from abjad import *


def test_instrumenttools_transpose_leaves_in_expr_from_fingered_pitch_to_sounding_pitch_01( ):

   staff = Staff("<c' e' g'>4 d'4 r4 e'4")
   instrumenttools.Clarinet( )(staff)

   for leaf in staff.leaves:
      leaf.pitch_indication_is_at_sounding_pitch = False

   instrumenttools.transpose_leaves_in_expr_from_fingered_pitch_to_sounding_pitch(staff)

   r'''
   \new Staff {
      \set Staff.instrumentName = \markup { Clarinet }
      \set Staff.shortInstrumentName = \markup { Cl. }
      <bf d' f'>4
      c'4
      r4
      d'4
   }
   '''

   for leaf in staff.leaves:
      if isinstance(leaf, (Note, Chord)):
         assert leaf.pitch_indication_is_at_sounding_pitch

   assert staff.format == "\\new Staff {\n\t\\set Staff.instrumentName = \\markup { Clarinet }\n\t\\set Staff.shortInstrumentName = \\markup { Cl. }\n\t<bf d' f'>4\n\tc'4\n\tr4\n\td'4\n}"
