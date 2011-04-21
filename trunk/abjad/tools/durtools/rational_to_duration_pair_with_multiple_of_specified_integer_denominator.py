from abjad.tools.durtools.rational_to_duration_pair_with_specified_integer_denominator import rational_to_duration_pair_with_specified_integer_denominator


def rational_to_duration_pair_with_multiple_of_specified_integer_denominator(
   duration, integer_denominator):
   '''.. versionadded: 1.1.1

   Change `duration` to duration pair with multiple of specified `integer_denominator`::

      abjad> durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 2)
      (1, 2)
      abjad> durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 4)
      (2, 4)
      abjad> durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 8)
      (4, 8)
      abjad> durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 16)
      (8, 16)

   ::

      abjad> durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 3)
      (3, 6)
      abjad> durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 6)
      (3, 6)
      abjad> durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 12)
      (6, 12)
      abjad> durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 24)
      (12, 24)

   ::

      abjad> durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 5)
      (5, 10)
      abjad> durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 10)
      (5, 10)
      abjad> durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 20)
      (10, 20)
      abjad> durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 40)
      (20, 40)

   .. versionchanged:: 1.1.2
      renamed ``durtools.in_terms_of_binary_multiple( )`` to
      ``durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator( )``.
   '''

   pair = rational_to_duration_pair_with_specified_integer_denominator(
      duration, integer_denominator)

   while not pair[-1] == integer_denominator:
      integer_denominator *= 2
      pair = rational_to_duration_pair_with_specified_integer_denominator(
         pair, integer_denominator)

   return pair
