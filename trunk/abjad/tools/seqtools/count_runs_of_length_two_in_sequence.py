from abjad.tools.seqtools.iterate_sequence_pairwise_strict import iterate_sequence_pairwise_strict


def count_runs_of_length_two_in_sequence(iterable):
   '''.. versionadded:: 1.1.2

   Return nonnegative integer number of two-element repetitions 
   in `iterable`. ::

      abjad> seqtools.count_runs_of_length_two_in_sequence([0, 0, 1, 1, 1, 2, 3, 4, 5])
      3

   .. versionchanged:: 1.1.2
      renamed ``seqtools.count_repetitions( )`` to
      ``seqtools.count_runs_of_length_two_in_sequence( )``.
   '''

   total_repetitions = 0
   for left, right in iterate_sequence_pairwise_strict(iterable):
      if left == right:
         total_repetitions += 1

   return total_repetitions
