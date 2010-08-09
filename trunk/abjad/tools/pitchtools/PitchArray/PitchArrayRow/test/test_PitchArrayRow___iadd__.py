from abjad import *


def test_PitchArrayRow___iadd___01( ):

   array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
   array[0].cells[0].pitches.append(0)
   array[0].cells[1].pitches.append(2)
   array[1].cells[2].pitches.append(4)

   '''
   [c'] [d'    ] [  ]
   [       ] [ ] [e']
   '''

   row = array[0].withdraw( )
   row += row

   '''
   [c'] [d'] [ ] [c'] [d'] [ ]
   '''

   assert row.cell_widths == (1, 2, 1, 1, 2, 1)
   assert row.dimensions == (1, 8)
   assert row.pitches == tuple(pitchtools.make_named_pitches_from_pitch_tokens([0, 2, 0, 2]))
