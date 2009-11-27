from abjad.rational import Rational


def is_pair(arg):
   '''True when `arg` has the form of a pair
   of integers that initialize a positive rational. ::

      abjad> durtools.is_duration_token((1, 4))
      True

   Otherwise false. ::

      abjad> durtools.is_pair((-1, 4))
      False
  
   ::

      abjad> durtools.is_pair((0, 1))
      False

   ::

      abjad> durtools.is_pair('foo')
      False
   '''

   if isinstance(arg, (list, tuple)) and len(arg) != 2:
      return False

   try:
      arg = Rational(*arg)
   except:
      return False

   if 0 < arg:
      return True
   else:
      return False
