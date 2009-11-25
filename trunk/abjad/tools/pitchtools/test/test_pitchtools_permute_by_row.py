from abjad import *


def test_pitchtools_permute_by_row_01( ):

   notes = [Note(p, (1, 4)) for p in (17, -10, -2, 11)]
   row = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
   row = [pitchtools.PitchClass(number) for number in row]

   notes = pitchtools.permute_by_row(notes, row)

   "[Note(bf, 4), Note(d, 4), Note(f'', 4), Note(b', 4)]"

   pcs = [pitchtools.PitchClass(number) for number in [10, 2, 5, 11]]
   assert [note.pitch.pc for note in notes] == pcs
