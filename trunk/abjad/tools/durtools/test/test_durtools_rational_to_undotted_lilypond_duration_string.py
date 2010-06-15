from abjad import *
import py.test


def test_durtools_rational_to_undotted_lilypond_duration_string_01( ):

   result = durtools.rational_to_undotted_lilypond_duration_string(Rational(1, 16))
   assert result == '16'

   result = durtools.rational_to_undotted_lilypond_duration_string(Rational(2, 16))
   assert result == '8'

   result = durtools.rational_to_undotted_lilypond_duration_string(Rational(3, 16))
   assert result == '8'

   result = durtools.rational_to_undotted_lilypond_duration_string(Rational(4, 16))
   assert result == '4'


def test_durtools_rational_to_undotted_lilypond_duration_string_02( ):

   assert py.test.raises(AssignabilityError,
      'durtools.rational_to_undotted_lilypond_duration_string(Rational(5, 16))')
