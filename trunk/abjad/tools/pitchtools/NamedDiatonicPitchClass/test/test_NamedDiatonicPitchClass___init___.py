from abjad import *


def test_NamedDiatonicPitchClass___init____01( ):
   '''Init named diatonic pitch class with diatonic pitch class name string.
   '''

   ndpc = pitchtools.NamedDiatonicPitchClass('c')
   assert isinstance(ndpc, pitchtools.NamedDiatonicPitchClass)

   
def test_NamedDiatonicPitchClass___init____02( ):
   '''Init named diatonic pitch class with diatonic pitch class number.
   '''

   ndpc = pitchtools.NamedDiatonicPitchClass(0)
   assert isinstance(ndpc, pitchtools.NamedDiatonicPitchClass)
