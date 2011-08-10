from abjad.tools.durtools.duration_token_to_rational import duration_token_to_rational


def duration_tokens_to_rationals(duration_tokens):
   '''.. versionadded:: 2.0

   Change `duration_tokens` to rationals::

      abjad> from abjad.tools import durtools

   ::

      abjad> durtools.duration_tokens_to_rationals([Fraction(2, 4), 3, '8.', (5, 16)])
      [Fraction(1, 2), Fraction(3, 1), Fraction(3, 16), Fraction(5, 16)]

   Return new object of `duration_tokens` type.
   '''

   return type(duration_tokens)([duration_token_to_rational(x) for x in duration_tokens])
