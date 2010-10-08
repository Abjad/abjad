from abjad import *
from abjad.tools import tonalitytools


def test_KeySignatureMark___init____01( ):
   '''Initialize with pitch class letter string and mode string.
   '''

   ks = contexttools.KeySignatureMark('g', 'major')
   
   assert ks.tonic == pitchtools.NamedChromaticPitchClass('g')
   assert ks.mode == tonalitytools.Mode('major')
