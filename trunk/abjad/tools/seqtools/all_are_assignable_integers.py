from abjad.tools import mathtools


def all_are_assignable_integers(expr):
   '''.. versionadded:: 1.1.2

   True when `expr` is a sequence and all elements in `expr` are notehead-assignable integers::

      abjad> seqtools.all_are_assignable_integers([1, 2, 3, 4, 6, 7, 8, 12, 14, 15, 16])
      True

   True when `expr` is an empty sequence::
   
      abjad> seqtools.all_are_assignable_integers([ ])
      True

   False otherwise::

      abjad> seqtools.all_are_assignable_integers('foo')
      False

   Return boolean.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.is_assignable( )`` to 
      ``seqtools.all_are_assignable_integers( )``.
   '''

   try:
      return all([mathtools.is_assignable_integer(x) for x in expr])
   except TypeError:
      return False
