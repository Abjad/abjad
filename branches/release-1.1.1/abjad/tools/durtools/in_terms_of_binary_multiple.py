from abjad.tools.durtools.in_terms_of import in_terms_of as \
   durtools_in_terms_of


def in_terms_of_binary_multiple(duration, desired_denominator):
   '''Docs.'''

   pair = durtools_in_terms_of(duration, desired_denominator)

   while not pair[-1] == desired_denominator:
      desired_denominator *= 2
      pair = durtools_in_terms_of(pair, desired_denominator)

   return pair
