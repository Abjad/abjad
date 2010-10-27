from abjad.tools.listtools.iterate_sequence_pairwise import iterate_sequence_pairwise


def is_repetition_free_sequence(iterable):
   '''.. versionadded:: 1.1.2

   True when ``iterable[i]`` does not equal ``iterable[i+1]`` for
   all ``iterable[i]`` in `iterable`. ::

      abjad> listtools.is_repetition_free_sequence([0, 1, 2, 6, 7, 8])
      True
   
   Otherwise false. ::

      abjad> listtools.is_repetition_free_sequence([0, 1, 2, 2, 7, 8])
      False

   .. versionchanged:: 1.1.2
      renamed ``listtools.is_repetition_free( )`` to
      ``listtools.is_repetition_free_sequence( )``.
   '''

   for left, right in iterate_sequence_pairwise(iterable):
      if left == right:
         return False
   return True
