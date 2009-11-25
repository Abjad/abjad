from abjad import *


def test_pitchtools_permute_by_row_01( ):

   notes = construct.notes([17, -10, -2, 11], [Rational(1, 4)])
   row = pitchtools.TwelveToneRow([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
   notes = pitchtools.permute_by_row(notes, row)

   "[Note(bf, 4), Note(d, 4), Note(f'', 4), Note(b', 4)]"

   pcs = [pitchtools.PitchClass(number) for number in [10, 2, 5, 11]]
   assert pitchtools.get_pitch_classes(notes) == tuple(pcs)
