from abjad.rational import Rational
from abjad.tools.durtools.is_duration_pair import is_duration_pair


def is_duration_token(duration_token):
   '''True when `duration_token` meets the criteria 
   for Abjad duration token.

   True when `duration_token` is a pair. ::

      abjad> durtools.is_duration_token((1, 4))
      True

   True when `duration_token` is a positive rational. ::

      abjad> durtools.is_duration_token(Rational(1, 4))
      True

   True when `duration_token` is a positive integer. ::

      abjad> durtools.is_duration_token(2)
      True

   Otherwise false. ::

      abjad> durtools.is_duration_token('foo')
      False
   '''

   if is_duration_pair(duration_token):
      return True
   elif isinstance(duration_token, Rational) and 0 < duration_token:
      return True
   elif isinstance(duration_token, (int, long)) and 0 < duration_token:
      return True
   else:
      return False
