from abjad.rational import Rational
from abjad.tools.durtools.is_assignable import is_assignable
from abjad.tools.durtools.naive_prolated_to_written import \
   naive_prolated_to_written
import math


#def prolated_to_written(prolated_duration, prolation = 'diminution'):
#   '''When ``prolation = 'diminution'`` return the greatest 
#   note_head-assignable rational less than or equal to 
#   `prolated_duration`. ::
#
#      abjad> for n in range(1, 17):
#      ...     prolated = Rational(n, 16)
#      ...     written = durtools.prolated_to_written(prolated)
#      ...     print '%s/16\t%s' % (n, written)
#      ... 
#      1/16    1/16
#      2/16    1/8
#      3/16    3/16
#      4/16    1/4
#      5/16    1/2
#      6/16    3/8
#      7/16    7/16
#      8/16    1/2
#      9/16    1
#      10/16   1
#      11/16   1
#      12/16   3/4
#      13/16   1
#      14/16   7/8
#      15/16   15/16
#      16/16   1
#
#   When ``prolation = 'augmentation'`` return the greatest 
#   note_head-assignable rational greater than or equal to 
#   `prolated_duration`. ::
#   
#      abjad> for n in range(1, 17):
#      ...     prolated = Rational(n, 16)
#      ...     written = durtools.prolated_to_written(prolated, 'augmentation')
#      ...     print '%s/16\t%s' % (n, written)
#      ... 
#      1/16    1/16
#      2/16    1/8
#      3/16    3/16
#      4/16    1/4
#      5/16    1/4
#      6/16    3/8
#      7/16    7/16
#      8/16    1/2
#      9/16    1/2
#      10/16   1/2
#      11/16   1/2
#      12/16   3/4
#      13/16   1/2
#      14/16   7/8
#      15/16   15/16
#      16/16   1
#
#   .. note:: this function returns dotted and double dotted durations
#      where possible.
#
#   .. note:: the output of this function does not increase monotonically.
#   '''
#
#   if is_assignable(prolated_duration):
#      return prolated_duration
#   else:
#      return naive_prolated_to_written(prolated_duration, prolation)
