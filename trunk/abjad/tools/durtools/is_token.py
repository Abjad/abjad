from abjad.rational import Rational
from abjad.tools.durtools.is_pair import is_pair


def is_token(arg):
   '''True when `arg` meets the criteria 
   for Abjad duration token.

   True when `arg` is a pair. ::

      abjad> durtools.is_token((1, 4))
      True

   True when `arg` is a positive rational. ::

      abjad> durtools.is_token(Rational(1, 4))
      True

   True when `arg` is a positive integer. ::

      abjad> durtools.is_token(2)
      True

   Otherwise false. ::

      abjad> durtools.is_token('foo')
      False
   '''

   if is_pair(arg):
      return True
   elif isinstance(arg, Rational) and 0 < arg:
      return True
   elif isinstance(arg, (int, long)) and 0 < arg:
      return True
   else:
      return False
