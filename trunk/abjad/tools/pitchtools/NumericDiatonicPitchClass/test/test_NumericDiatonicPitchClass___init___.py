from abjad import *


def test_NumericDiatonicPitchClass___init____01( ):
   '''Init numeric diatonic pitch class from diatonic pitch class number.
   '''

   dpc = pitchtools.NumericDiatonicPitchClass(0)
   #assert dpc.diatonic_pitch_class_number == 0
   assert isinstance(dpc, pitchtools.NumericDiatonicPitchClass)


def test_NumericDiatonicPitchClass___init____02( ):
   '''Init numeric diatonic pitch class from diatonic pitch class name.
   '''

   dpc = pitchtools.NumericDiatonicPitchClass('c')
   #assert dpc.diatonic_pitch_class_number == 0
   assert isinstance(dpc, pitchtools.NumericDiatonicPitchClass)
