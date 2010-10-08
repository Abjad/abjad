from abjad import *


def test_NamedChromaticPitchClass_letter_01( ):
   
   assert pitchtools.NamedChromaticPitchClass('c').letter == 'c'
   assert pitchtools.NamedChromaticPitchClass('cqs').letter == 'c'
   assert pitchtools.NamedChromaticPitchClass('cqf').letter == 'c'
   assert pitchtools.NamedChromaticPitchClass('cs').letter == 'c'
   assert pitchtools.NamedChromaticPitchClass('cf').letter == 'c'
   assert pitchtools.NamedChromaticPitchClass('ctqs').letter == 'c'
   assert pitchtools.NamedChromaticPitchClass('ctqf').letter == 'c'
   assert pitchtools.NamedChromaticPitchClass('css').letter == 'c'
   assert pitchtools.NamedChromaticPitchClass('cff').letter == 'c'
