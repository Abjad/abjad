from abjad.tools.mathtools.is_assignable import is_assignable \
   as mathtools_is_assignable

def is_assignable(l):
   '''.. versionadded:: 1.1.2

   True when the elements of `l` are all notehead assignable. ::

      abjad> l = [1, 2, 3, 4, 6, 7, 8, 12, 14, 15, 16]
      abjad> listtools.is_assignable(l)
      True

   False when the elements of `l` are not all notehead assignable. ::

      abjad> l = [5, 9, 10, 11, 13]
      abjad> listtools.is_assignable(l)
      False

   ::

      abjad> l = [4, 4, 4, 4, 5, 4, 4]
      abjad> listtools.is_assignable(l)
      False

   True by definition when `l` is empty. ::
   
      abjad> l = [ ]
      abjad> listtools.is_assignable(l)
      True
   '''

   return all([mathtools_is_assignable(x) for x in l])
