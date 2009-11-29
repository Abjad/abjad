from abjad import *
import py.test
py.test.skip( )


def test_pitchtools_DiatonicInterval_semitones_01( ):

   assert pitchtools.DiatonicInterval('perfect', 1).semitones == 0
   assert pitchtools.DiatonicInterval('minor', 2).semitones == 1
   assert pitchtools.DiatonicInterval('major', 2).semitones == 2
   assert pitchtools.DiatonicInterval('minor', 3).semitones == 3
   assert pitchtools.DiatonicInterval('major', 3).semitones == 4
   assert pitchtools.DiatonicInterval('perfect', 4).semitones == 5
   assert pitchtools.DiatonicInterval('augmented', 4).semitones == 6
   assert pitchtools.DiatonicInterval('diminished', 5).semitones == 6
   assert pitchtools.DiatonicInterval('perfect', 5).semitones == 7
   assert pitchtools.DiatonicInterval('minor', 6).semitones == 8
   assert pitchtools.DiatonicInterval('major', 6).semitones == 9
   assert pitchtools.DiatonicInterval('minor', 7).semitones == 10
   assert pitchtools.DiatonicInterval('major', 7).semitones == 11
   assert pitchtools.DiatonicInterval('perfect', 8).semitones == 12


def test_pitchtools_DiatonicInterval_semitones_02( ):

   assert pitchtools.DiatonicInterval('major', 23).semitones == 38
   assert pitchtools.DiatonicInterval('major', -23).semitones == -38
