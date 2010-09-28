from abjad.core import Fraction


def is_duration_pair(arg):
   '''True when `arg` has the form of a pair
   of integers that initialize a positive rational. ::

      abjad> durtools.is_duration_pair((1, 4))
      True

   Otherwise false. ::

      abjad> durtools.is_duration_pair((-1, 4))
      False
  
   ::

      abjad> durtools.is_duration_pair((0, 1))
      False

   ::

      abjad> durtools.is_duration_pair('foo')
      False

   .. versionchanged:: 1.1.2
      renamed ``durtools.is_pair( )`` to ``durtools.is_duration_pair( )``.
   '''

   if isinstance(arg, (list, tuple)) and len(arg) != 2:
      return False

   try:
      arg = Fraction(*arg)
   except:
      return False

   if 0 < arg:
      return True
   else:
      return False
