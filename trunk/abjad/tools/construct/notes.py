from abjad.helpers.agglomerate_durations_by_prolation import \
     _agglomerate_durations_by_prolation
from abjad.helpers.duration_token_unpack import _duration_token_unpack
from abjad.helpers.is_duration_token import _is_duration_token
from abjad.helpers.is_pitch_token import is_pitch_token
from abjad.helpers.next_least_power_of_two import _next_least_power_of_two
from abjad.helpers.resize_list import _resize_list
from abjad.rational.rational import Rational
from abjad.tools.construct.helpers import _construct_unprolated_notes
from abjad.tools import mathtools
from abjad.tuplet.fm.tuplet import FixedMultiplierTuplet
import operator
import math
      
def notes(pitches, durations, direction='big-endian'):
   '''Constructs a list of prolated notes of length len(durations).

      Parameters:
      pitches:    a single pitch or a list/tuple of pitches. If the list is
                  smaller than that of the durations, the pitches are cycled 
                  through.
      durations:  a sinlge duration or a list of durations. 
                  The durations need not be of the form m / 2**n 
                  and may be any rational value.
      direction:  may be 'big-endian' or 'little-endian'.
                  'big-endian' returns list of notes of decreasing duration.
                  'little-endian' returns list of notes of increasing duration.
   '''

   if is_pitch_token(pitches):
      pitches = [pitches]
   
   if _is_duration_token(durations):
      durations = [durations]

   # this block is a hack to allow the function to accept a Rational
   # as the duration input parameter; better will be to change
   # the rest of the implementation to allow for Rationals directly.
   ## [VA] We don't want to convert to Rationals internally because
   ## Rationals reduce fractions to their minimum expression. e.g. 
   ## (3, 3) --> Rational(1, 1), and we sometimes generate duration
   ## tokens that are not reduced, so we want to preserve the denominator 3.
   durations = [_duration_token_unpack(dur) for dur in durations]

   ## set lists of pitches and durations to the same length
   size = max(len(durations), len(pitches))
   durations = _resize_list(durations, size)
   pitches = _resize_list(pitches, size)

   durations = _agglomerate_durations_by_prolation(durations)

   result = [ ]
   for ds in durations:
      ## get factors in denominator of duration group ds other than 1, 2.
      factors = set(mathtools.factors(ds[0][1]))
      factors.discard(1)
      factors.discard(2)
      ps = pitches[0:len(ds)]
      pitches = pitches[len(ds):]
      if len(factors) == 0:
         result.extend(_construct_unprolated_notes(ps, ds, direction))
      else:
         ## compute prolation
         #denominator = reduce(operator.mul, factors)
         denominator = ds[0][1]
         numerator = _next_least_power_of_two(denominator)
         multiplier = (numerator, denominator)
         ratio = 1 / Rational(*multiplier)
         ds = [ratio * Rational(*d) for d in ds]
         ## make notes
         ns = _construct_unprolated_notes(ps, ds, direction)
         t = FixedMultiplierTuplet(multiplier, ns)
         result.append(t)
   return result
      

