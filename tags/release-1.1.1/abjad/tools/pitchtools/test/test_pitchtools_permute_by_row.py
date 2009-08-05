from abjad import *


def test_pitchtools_permute_by_row_01( ):

   notes = [Note(p, (1, 4)) for p in (17, -10, -2, 11)]
   row = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]

   t = pitchtools.permute_by_row(notes, row)

   "[Note(bf, 4), Note(d, 4), Note(f'', 4), Note(b', 4)]"

   assert [x.pitch.pc for x in t] == [10, 2, 5, 11]
