from abjad import *


def test_PitchClass_semitones_01( ):

   assert pitchtools.PitchClass(0).semitones == 0
   assert pitchtools.PitchClass(0.5).semitones == 0.5
   assert pitchtools.PitchClass(1).semitones == 1
   assert pitchtools.PitchClass(1.5).semitones == 1.5


def test_PitchClass_semitones_02( ):

   assert pitchtools.PitchClass(12).semitones == 0
   assert pitchtools.PitchClass(12.5).semitones == 0.5
   assert pitchtools.PitchClass(13).semitones == 1
   assert pitchtools.PitchClass(13.5).semitones == 1.5
