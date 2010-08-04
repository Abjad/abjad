from abjad import *


def test_PitchArrayRow_append_01( ):
   '''Append cell by positive integer width.'''

   array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
   array[0].cells[0].pitches.append(pitchtools.NamedPitch(0))
   array[0].cells[1].pitches.extend([pitchtools.NamedPitch(2), pitchtools.NamedPitch(4)])

   '''
   [c'] [d' e'    ] [ ]
   [          ] [ ] [ ]
   '''
   
   array[0].append(1)
   array[1].append(1)

   '''
   [c'] [d' e'    ] [ ] [ ]
   [          ] [ ] [ ] [ ]
   '''

   assert str(array) == "[c'] [d' e'    ] [ ] [ ]\n[          ] [ ] [ ] [ ]"


def test_PitchArrayRow_append_02( ):

   array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
   array[0].cells[0].pitches.append(pitchtools.NamedPitch(0))
   array[0].cells[1].pitches.extend([pitchtools.NamedPitch(2), pitchtools.NamedPitch(4)])

   '''
   [c'] [d' e'    ] [ ]
   [          ] [ ] [ ]
   '''
   
   array[0].append(pitchtools.NamedPitch(0))
   array[1].append(pitchtools.NamedPitch(2))

   '''
   [c'] [d' e'    ] [ ] [c']
   [          ] [ ] [ ] [d']
   '''

   assert str(array) == "[c'] [d' e'    ] [ ] [c']\n[          ] [ ] [ ] [d']"
