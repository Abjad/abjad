from abjad import *


def test_NamedPitchClass_letter_01( ):
   
   assert pitchtools.NamedPitchClass('c').letter == 'c'
   assert pitchtools.NamedPitchClass('cqs').letter == 'c'
   assert pitchtools.NamedPitchClass('cqf').letter == 'c'
   assert pitchtools.NamedPitchClass('cs').letter == 'c'
   assert pitchtools.NamedPitchClass('cf').letter == 'c'
   assert pitchtools.NamedPitchClass('ctqs').letter == 'c'
   assert pitchtools.NamedPitchClass('ctqf').letter == 'c'
   assert pitchtools.NamedPitchClass('css').letter == 'c'
   assert pitchtools.NamedPitchClass('cff').letter == 'c'
