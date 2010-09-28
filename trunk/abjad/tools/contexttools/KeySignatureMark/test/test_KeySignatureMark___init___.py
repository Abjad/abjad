from abjad import *


def test_KeySignatureMark___init____01( ):
   '''Initialize with pitch class letter string and mode string.
   '''

   ks = marktools.KeySignatureMark('g', 'major')
   
   assert ks.tonic == pitchtools.NamedPitchClass('g')
   assert ks.mode == tonalitytools.Mode('major')
