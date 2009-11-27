from abjad import *


def test_pitchtools_get_pitches_01( ):
   '''Works with containers.'''

   tuplet = FixedDurationTuplet((2, 8), construct.scale(3))
   t = pitchtools.get_pitches(tuplet)

   assert t == (Pitch('c', 4), Pitch('d', 4), Pitch('e', 4))


def test_pitchtools_get_pitches_02( ):
   '''Works with spanners.'''

   staff = Staff(construct.scale(4))
   beam = Beam(staff[:])
   t = pitchtools.get_pitches(beam)

   assert t == (Pitch('c', 4), Pitch('d', 4), Pitch('e', 4), Pitch('f', 4))


def test_pitchtools_get_pitches_03( ):
   '''Works with pitch sets.'''

   pitch_set = pitchtools.PitchSet([0, 2, 4, 5])
   t = pitchtools.get_pitches(pitch_set)

   assert t == (Pitch('c', 4), Pitch('d', 4), Pitch('e', 4), Pitch('f', 4))


def test_pitchtools_get_pitches_04( ):
   '''Works with pitch arrays.'''

   array = pitchtools.PitchArray([
      [1, (2, 1), (-1.5, 2)],
      [(7, 2), (6, 1), 1],
      ]) 

   '''
   [  ] [d'] [bqf    ]
   [g'     ] [fs'] [ ]
   '''

   assert pitchtools.get_pitches(array) == (
      Pitch('d', 4), Pitch('bqf', 3), Pitch('fs', 4), Pitch('g', 4))
