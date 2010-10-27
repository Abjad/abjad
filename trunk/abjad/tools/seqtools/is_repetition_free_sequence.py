from abjad.tools.seqtools.iterate_sequence_pairwise_strict import iterate_sequence_pairwise_strict


def is_repetition_free_sequence(iterable):
   '''.. versionadded:: 1.1.2

   True when ``iterable[i]`` does not equal ``iterable[i+1]`` for
   all ``iterable[i]`` in `iterable`. ::

      abjad> seqtools.is_repetition_free_sequence([0, 1, 2, 6, 7, 8])
      True
   
   Otherwise false. ::

      abjad> seqtools.is_repetition_free_sequence([0, 1, 2, 2, 7, 8])
      False

   .. versionchanged:: 1.1.2
      renamed ``seqtools.is_repetition_free( )`` to
      ``seqtools.is_repetition_free_sequence( )``.
   '''

   for left, right in iterate_sequence_pairwise_strict(iterable):
      if left == right:
         return False
   return True
