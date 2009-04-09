from abjad.rational.rational import Rational
from abjad.tools.durtools.is_assignable import is_assignable
from abjad.tools.durtools.naive_prolated_to_written import \
   naive_prolated_to_written
import math


def prolated_to_written(prolated_duration, prolation = 'diminution'):
   '''Wrapper around durtools.naive_prolated_to_written ).
      This smarter durtools.prolated_to_written( ) will return dotted or
      double dotted written durations, if possible.

      Note that output does not increase monotonically.'''

   if is_assignable(prolated_duration):
      return prolated_duration
   else:
      return naive_prolated_to_written(prolated_duration, prolation)
