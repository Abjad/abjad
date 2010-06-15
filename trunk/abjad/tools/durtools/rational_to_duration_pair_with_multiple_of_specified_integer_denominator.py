from abjad.tools.durtools.rational_to_duration_pair_with_specified_integer_denominator import rational_to_duration_pair_with_specified_integer_denominator


def rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, desired_denominator):
   '''Return `duration` as a pair with denominator equal to
   the least common multiple of `desired_denominator` 
   and the denominator of `duration`. ::

      abjad> durtools.rational_to_duration_pair_with_specified_integer_denominator_binary_multiple(Rational(1, 2), 2)
      (1, 2)
      abjad> durtools.rational_to_duration_pair_with_specified_integer_denominator_binary_multiple(Rational(1, 2), 4)
      (2, 4)
      abjad> durtools.rational_to_duration_pair_with_specified_integer_denominator_binary_multiple(Rational(1, 2), 8)
      (4, 8)
      abjad> durtools.rational_to_duration_pair_with_specified_integer_denominator_binary_multiple(Rational(1, 2), 16)
      (8, 16)

   ::

      abjad> durtools.rational_to_duration_pair_with_specified_integer_denominator_binary_multiple(Rational(1, 2), 3)
      (3, 6)
      abjad> durtools.rational_to_duration_pair_with_specified_integer_denominator_binary_multiple(Rational(1, 2), 6)
      (3, 6)
      abjad> durtools.rational_to_duration_pair_with_specified_integer_denominator_binary_multiple(Rational(1, 2), 12)
      (6, 12)
      abjad> durtools.rational_to_duration_pair_with_specified_integer_denominator_binary_multiple(Rational(1, 2), 24)
      (12, 24)

   ::

      abjad> durtools.rational_to_duration_pair_with_specified_integer_denominator_binary_multiple(Rational(1, 2), 5)
      (5, 10)
      abjad> durtools.rational_to_duration_pair_with_specified_integer_denominator_binary_multiple(Rational(1, 2), 10)
      (5, 10)
      abjad> durtools.rational_to_duration_pair_with_specified_integer_denominator_binary_multiple(Rational(1, 2), 20)
      (10, 20)
      abjad> durtools.rational_to_duration_pair_with_specified_integer_denominator_binary_multiple(Rational(1, 2), 40)

   .. versionchanged:: 1.1.2
      renamed ``durtools.in_terms_of_binary_multiple( )`` to
      ``durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator( )``.

   .. versionchanged:: 1.1.2
      renamed ``durtools.rational_to_duration_pair_with_multiple_of_integer_denominator( )`` to
      ``durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator( )``.
   '''

   pair = rational_to_duration_pair_with_specified_integer_denominator(duration, desired_denominator)

   while not pair[-1] == desired_denominator:
      desired_denominator *= 2
      pair = rational_to_duration_pair_with_specified_integer_denominator(pair, desired_denominator)

   return pair
