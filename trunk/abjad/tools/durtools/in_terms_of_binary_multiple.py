from abjad.tools.durtools.in_terms_of import in_terms_of


def in_terms_of_binary_multiple(duration, desired_denominator):
   '''Return `duration` as a pair with denominator equal to
   the least common multiple of `desired_denominator` 
   and the denominator of `duration`. ::

      abjad> durtools.in_terms_of_binary_multiple(Rational(1, 2), 2)
      (1, 2)
      abjad> durtools.in_terms_of_binary_multiple(Rational(1, 2), 4)
      (2, 4)
      abjad> durtools.in_terms_of_binary_multiple(Rational(1, 2), 8)
      (4, 8)
      abjad> durtools.in_terms_of_binary_multiple(Rational(1, 2), 16)
      (8, 16)

   ::

      abjad> durtools.in_terms_of_binary_multiple(Rational(1, 2), 3)
      (3, 6)
      abjad> durtools.in_terms_of_binary_multiple(Rational(1, 2), 6)
      (3, 6)
      abjad> durtools.in_terms_of_binary_multiple(Rational(1, 2), 12)
      (6, 12)
      abjad> durtools.in_terms_of_binary_multiple(Rational(1, 2), 24)
      (12, 24)

   ::

      abjad> durtools.in_terms_of_binary_multiple(Rational(1, 2), 5)
      (5, 10)
      abjad> durtools.in_terms_of_binary_multiple(Rational(1, 2), 10)
      (5, 10)
      abjad> durtools.in_terms_of_binary_multiple(Rational(1, 2), 20)
      (10, 20)
      abjad> durtools.in_terms_of_binary_multiple(Rational(1, 2), 40)
   '''

   pair = in_terms_of(duration, desired_denominator)

   while not pair[-1] == desired_denominator:
      desired_denominator *= 2
      pair = in_terms_of(pair, desired_denominator)

   return pair
