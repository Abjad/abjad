from abjad import *


def test_NumericDiatonicPitchClass___init____01( ):
   '''Init numeric diatonic pitch class from diatonic pitch class number.
   '''

   numeric_diatonic_pitch_class = pitchtools.NumericDiatonicPitchClass(0)
   assert isinstance(numeric_diatonic_pitch_class, pitchtools.NumericDiatonicPitchClass)

   numeric_diatonic_pitch_class = pitchtools.NumericDiatonicPitchClass(0.0)
   assert isinstance(numeric_diatonic_pitch_class, pitchtools.NumericDiatonicPitchClass)

   numeric_diatonic_pitch_class = pitchtools.NumericDiatonicPitchClass(Fraction(0))
   assert isinstance(numeric_diatonic_pitch_class, pitchtools.NumericDiatonicPitchClass)


def test_NumericDiatonicPitchClass___init____02( ):
   '''Init numeric diatonic pitch class from diatonic pitch class name.
   '''

   diatonic_pitch_class = pitchtools.NumericDiatonicPitchClass('c')
   assert isinstance(diatonic_pitch_class, pitchtools.NumericDiatonicPitchClass)


def test_NumericDiatonicPitchClass___init____03( ):
   '''Init numeric diatonic pitch class from diatonic pitch class.
   '''

   diatonic_pitch_class_1 = pitchtools.NumericDiatonicPitchClass(0)
   diatonic_pitch_class_2 = pitchtools.NumericDiatonicPitchClass(diatonic_pitch_class_1)
   assert isinstance(diatonic_pitch_class_2, pitchtools.NumericDiatonicPitchClass)
