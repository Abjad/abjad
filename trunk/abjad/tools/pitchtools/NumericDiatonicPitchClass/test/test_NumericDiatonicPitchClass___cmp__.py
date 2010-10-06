from abjad import *
import py.test


def test_NumericDiatonicPitchClass___cmp___01( ):
   '''Compare equal numeric diatonic pitch-classes.
   '''

   numeric_diatonic_pitch_class_1 = pitchtools.NumericDiatonicPitchClass(0)
   numeric_diatonic_pitch_class_2 = pitchtools.NumericDiatonicPitchClass(0)

   assert     numeric_diatonic_pitch_class_1 == numeric_diatonic_pitch_class_2
   assert not numeric_diatonic_pitch_class_1 != numeric_diatonic_pitch_class_2

   comparison_string = 'numeric_diatonic_pitch_class_1 <  numeric_diatonic_pitch_class_2'
   assert py.test.raises(NotImplementedError, comparison_string)
   comparison_string = 'numeric_diatonic_pitch_class_1 <= numeric_diatonic_pitch_class_2'
   assert py.test.raises(NotImplementedError, comparison_string)
   comparison_string = 'numeric_diatonic_pitch_class_1 >  numeric_diatonic_pitch_class_2'
   assert py.test.raises(NotImplementedError, comparison_string)
   comparison_string = 'numeric_diatonic_pitch_class_1 >= numeric_diatonic_pitch_class_2'
   assert py.test.raises(NotImplementedError, comparison_string)


def test_NumericDiatonicPitchClass___cmp___02( ):
   '''Compare numeric diatonic pitch-class to equivalent diatonic pitch-class number.
   '''

   numeric_diatonic_pitch_class_1 = pitchtools.NumericDiatonicPitchClass(0)
   diatonic_pitch_class_number = 0

   assert     numeric_diatonic_pitch_class_1 == diatonic_pitch_class_number
   assert not numeric_diatonic_pitch_class_1 != diatonic_pitch_class_number

   comparison_string = 'numeric_diatonic_pitch_class_1 <  diatonic_pitch_class_number'
   assert py.test.raises(NotImplementedError, comparison_string)
   comparison_string = 'numeric_diatonic_pitch_class_1 <= diatonic_pitch_class_number'
   assert py.test.raises(NotImplementedError, comparison_string)
   comparison_string = 'numeric_diatonic_pitch_class_1 >  diatonic_pitch_class_number'
   assert py.test.raises(NotImplementedError, comparison_string)
   comparison_string = 'numeric_diatonic_pitch_class_1 >= diatonic_pitch_class_number'
   assert py.test.raises(NotImplementedError, comparison_string)


def test_NumericDiatonicPitchClass___cmp___03( ):
   '''Compare unequal numeric diatonic pitch-classes.
   '''

   numeric_diatonic_pitch_class_1 = pitchtools.NumericDiatonicPitchClass(0)
   numeric_diatonic_pitch_class_2 = pitchtools.NumericDiatonicPitchClass(1)

   assert not numeric_diatonic_pitch_class_1 == numeric_diatonic_pitch_class_2
   assert     numeric_diatonic_pitch_class_1 != numeric_diatonic_pitch_class_2

   comparison_string = 'numeric_diatonic_pitch_class_1 <  numeric_diatonic_pitch_class_2'
   assert py.test.raises(NotImplementedError, comparison_string)
   comparison_string = 'numeric_diatonic_pitch_class_1 <= numeric_diatonic_pitch_class_2'
   assert py.test.raises(NotImplementedError, comparison_string)
   comparison_string = 'numeric_diatonic_pitch_class_1 >  numeric_diatonic_pitch_class_2'
   assert py.test.raises(NotImplementedError, comparison_string)
   comparison_string = 'numeric_diatonic_pitch_class_1 >= numeric_diatonic_pitch_class_2'
   assert py.test.raises(NotImplementedError, comparison_string)


def test_NumericDiatonicPitchClass___cmp___04( ):
   '''Compare numeric diatonic pitch-class to unequal diatonic pitch-class number.
   '''

   numeric_diatonic_pitch_class_1 = pitchtools.NumericDiatonicPitchClass(0)
   diatonic_pitch_class_number = 1

   assert not numeric_diatonic_pitch_class_1 == diatonic_pitch_class_number
   assert     numeric_diatonic_pitch_class_1 != diatonic_pitch_class_number

   comparison_string = 'numeric_diatonic_pitch_class_1 <  diatonic_pitch_class_number'
   assert py.test.raises(NotImplementedError, comparison_string)
   comparison_string = 'numeric_diatonic_pitch_class_1 <= diatonic_pitch_class_number'
   assert py.test.raises(NotImplementedError, comparison_string)
   comparison_string = 'numeric_diatonic_pitch_class_1 >  diatonic_pitch_class_number'
   assert py.test.raises(NotImplementedError, comparison_string)
   comparison_string = 'numeric_diatonic_pitch_class_1 >= diatonic_pitch_class_number'
   assert py.test.raises(NotImplementedError, comparison_string)
