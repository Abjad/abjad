from abjad.tools import mathtools


def all_are_assignable_integers(l):
   '''.. versionadded:: 1.1.2

   True when the elements of `l` are all notehead assignable. ::

      abjad> l = [1, 2, 3, 4, 6, 7, 8, 12, 14, 15, 16]
      abjad> listtools.all_are_assignable_integers(l)
      True

   False when the elements of `l` are not all notehead assignable. ::

      abjad> l = [5, 9, 10, 11, 13]
      abjad> listtools.all_are_assignable_integers(l)
      False

   ::

      abjad> l = [4, 4, 4, 4, 5, 4, 4]
      abjad> listtools.all_are_assignable_integers(l)
      False

   True by definition when `l` is empty. ::
   
      abjad> l = [ ]
      abjad> listtools.all_are_assignable_integers(l)
      True

   .. versionchanged:: 1.1.2
      renamed ``listtools.is_assignable( )`` to 
      ``listtools.all_are_assignable_integers( )``.

   .. versionchanged:: 1.1.2
      renamed ``listtools.are_assignable_integers( )`` to
      ``listtools.all_are_assignable_integers( )``.
   '''

   return all([mathtools.is_assignable_integer(x) for x in l])
