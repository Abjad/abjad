from abjad import *
import py.test


def test_durtools_assignable_rational_to_lilypond_duration_string_01( ):

   assert durtools.assignable_rational_to_lilypond_duration_string(Rational(1, 16)) == '16' 
   assert durtools.assignable_rational_to_lilypond_duration_string(Rational(2, 16)) == '8' 
   assert durtools.assignable_rational_to_lilypond_duration_string(Rational(3, 16)) == '8.' 
   assert durtools.assignable_rational_to_lilypond_duration_string(Rational(4, 16)) == '4' 


def test_durtools_assignable_rational_to_lilypond_duration_string_02( ):

   assert py.test.raises(AssignabilityError,
      'durtools.assignable_rational_to_lilypond_duration_string(Rational(5, 16))')
