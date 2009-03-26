from abjad.helpers.is_assignable import is_assignable
from abjad.helpers.naive_prolated_to_written import _naive_prolated_to_written


def _prolated_to_written(prolated_duration, prolation = 'diminution'):
   '''Wrapper around _naive_prolated_to_written( ).
      This smarter _prolated_to_written( ) will return dotted or
      double dotted written durations, if possible.

      Note that output does not increase monotonically.'''

   if is_assignable(prolated_duration):
      return prolated_duration
   else:
      return _naive_prolated_to_written(prolated_duration, prolation)
