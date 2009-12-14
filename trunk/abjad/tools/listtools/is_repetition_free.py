from abjad.tools.listtools.pairwise import pairwise


def is_repetition_free(iterable):
   '''.. versionadded:: 1.1.2

   True when ``iterable[i]`` does not equal ``iterable[i+1]`` for
   all ``iterable[i]`` in `iterable`. ::

      abjad> listtools.is_repetition_free([0, 1, 2, 6, 7, 8])
      True
   
   Otherwise false. ::

      abjad> listtools.is_repetition_free([0, 1, 2, 2, 7, 8])
      False
   '''

   for left, right in pairwise(iterable):
      if left == right:
         return False
   return True
