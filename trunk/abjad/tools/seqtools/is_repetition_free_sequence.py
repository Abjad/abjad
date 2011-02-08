from abjad.tools.seqtools.iterate_sequence_pairwise_strict import iterate_sequence_pairwise_strict


def is_repetition_free_sequence(expr):
   '''.. versionadded:: 1.1.2

   True when `expr` is a sequence and `expr` is repetition free::

      abjad> seqtools.is_repetition_free_sequence([0, 1, 2, 6, 7, 8])
      True
   
   False when `expr` is a sequence and `expr` is not repetition free::

      abjad> seqtools.is_repetition_free_sequence([0, 1, 2, 2, 7, 8])
      False

   True when `expr` is an empty sequence::

      abjad> seqtools.is_repetition_free_sequence([ ])
      True

   False `expr` is not a sequence::

      abjad> seqtools.is_repetition_free_sequence(17)
      False

   .. versionchanged:: 1.1.2
      renamed ``seqtools.is_repetition_free( )`` to
      ``seqtools.is_repetition_free_sequence( )``.
   '''

   try:
      for left, right in iterate_sequence_pairwise_strict(expr):
         if left == right:
            return False
      return True

   except TypeError:
      return False
