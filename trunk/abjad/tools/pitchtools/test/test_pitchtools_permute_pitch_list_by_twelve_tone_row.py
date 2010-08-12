from abjad import *


def test_pitchtools_permute_pitch_list_by_twelve_tone_row_01( ):

   notes = notetools.make_notes([17, -10, -2, 11], [Rational(1, 4)])
   row = pitchtools.TwelveToneRow([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
   notes = pitchtools.permute_pitch_list_by_twelve_tone_row(notes, row)

   "[Note(bf, 4), Note(d, 4), Note(f'', 4), Note(b', 4)]"

   pcs = [pitchtools.NumericPitchClass(number) for number in [10, 2, 5, 11]]
   assert pitchtools.list_numeric_pitch_classes_in_expr(notes) == tuple(pcs)
