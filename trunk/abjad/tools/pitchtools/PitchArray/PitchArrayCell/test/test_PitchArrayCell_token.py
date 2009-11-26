from abjad import *



def test_PitchArrayCell_token_01( ):

   array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
   array[0].cells[0].pitches.append(Pitch(0))
   array[0].cells[1].pitches.extend([Pitch(2), Pitch(4)])

   '''
   [c'] [d' e'    ] [ ]
   [          ] [ ] [ ]
   '''

   assert array[0].cells[0].token == Pitch(0)
   assert array[0].cells[1].token == ([Pitch(2), Pitch(4)], 2)
   assert array[0].cells[2].token == 1

   assert array[1].cells[0].token == 2
   assert array[1].cells[1].token == 1
   assert array[1].cells[2].token == 1
