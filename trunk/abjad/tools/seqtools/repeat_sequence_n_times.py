from abjad.tools import mathtools
import copy


def repeat_sequence_n_times(sequence, n):
   '''.. versionadded:: 1.1.2

   Repeat `sequence` `n` times::

      abjad> seqtools.repeat_sequence_n_times((1, 2, 3, 4, 5), 3)
      (1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5)

   Repeat `sequence` ``0`` times::

      abjad> seqtools.repeat_sequence_n_times((1, 2, 3, 4, 5), 0)
      ( )

   Return newly constructed `sequence` type of copied `sequence` elements.

   .. versionchanged:: 1.1.2
      renamed ``listtools.repeat_n_cycles( )`` to
      ``seqtools.repeat_sequence_n_times( )``.
   '''

   if not mathtools.is_nonnegative_integer(n):
      raise ValueError('must be nonnegative integer.')

   result = [ ]
   for x in range(n):
      for element in sequence:
         result.append(copy.copy(element))
   return type(sequence)(result)
