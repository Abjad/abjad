from abjad.tools.seqtools.flatten_sequence import flatten_sequence
from abjad.tools.seqtools.zip_sequences_nontruncating import zip_sequences_nontruncating


def interlace_sequences(*sequences):
   '''.. versionadded:: 1.1.1

   Interlace `sequences`::

      k = range(100, 103)
      l = range(200, 201)
      m = range(300, 303)
      n = range(400, 408)
      t = seqtools.interlace_sequences(k, l, m, n)
      [100, 200, 300, 400, 101, 301, 401, 102, 302, 402, 403, 404, 405, 406, 407]

   Return list.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.interlace( )`` to
      ``seqtools.interlace_sequences( )``.
   '''

   zipped_sequences = zip_sequences_nontruncating(*sequences)
   flattened_sequences = flatten_sequence(zipped_sequences, depth = 1)

   return flattened_sequences
