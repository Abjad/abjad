from fractions import Fraction
from abjad.tools import durtools
from abjad.tools import listtools
from abjad.tools import mathtools
from abjad.tools import pitchtools
#from abjad.components.Tuplet import Tuplet
from abjad.components.Tuplet import Tuplet
import operator
import math
      

def make_notes(pitches, durations, direction='big-endian'):
   '''Constructs a list of prolated notes with length 
   equal to length of `durations.`

   Parameters:

   `pitches`
      a single pitch or a list/tuple of pitches. If the list is
      smaller than that of the durations, the pitches are cycled through.

   `durations`
      a sinlge duration or a list of durations. 
      The durations need not be of the form ``m / 2**n``
      and may be any rational value.

   `direction`
      may be 'big-endian' or 'little-endian'.
      'big-endian' returns list of notes of decreasing duration.
      'little-endian' returns list of notes of increasing duration.

   ::

      abjad> notetools.make_notes(0, [(1, 16), (1, 8), (1, 8)])
      [Note(c', 16), Note(c', 8), Note(c', 8)]

   .. versionchanged:: 1.1.2
      renamed ``construct.notes( )`` to
      ``notetools.make_notes( )``.

   .. versionchanged:: 1.1.2
      renamed ``leaftools.make_notes( )`` to
      ``notetools.make_notes( )``.
   '''
   from abjad.tools.leaftools._construct_unprolated_notes import _construct_unprolated_notes

   if pitchtools.is_named_chromatic_pitch_token(pitches):
      pitches = [pitches]
   
   if durtools.is_duration_token(durations):
      durations = [durations]

   # this block is a hack to allow the function to accept a Fraction
   # as the duration input parameter; better will be to change
   # the rest of the implementation to allow for Fractions directly.
   ## [VA] We don't want to convert to Fractions internally because
   ## Fractions reduce fractions to their minimum expression. e.g. 
   ## (3, 3) --> Fraction(1, 1), and we sometimes generate duration
   ## tokens that are not reduced, so we want to preserve the denominator 3.
   ## [TB] When do we want (3, 3) instead of (1, 1)?
   ## Durations should always reduce;
   ## So tokens can represent tuplet multipliers or something
   ## else that shouldn't reduce?
   durations = [durtools.duration_token_to_reduced_duration_pair(dur) for dur in durations]

   ## set lists of pitches and durations to the same length
   size = max(len(durations), len(pitches))
   durations = listtools.repeat_list_to_length(durations, size)
   pitches = listtools.repeat_list_to_length(pitches, size)

   durations = durtools.group_duration_tokens_by_implied_prolation(durations)

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
         numerator = mathtools.greatest_power_of_two_less_equal(denominator)
         multiplier = (numerator, denominator)
         ratio = 1 / Fraction(*multiplier)
         ds = [ratio * Fraction(*d) for d in ds]
         ## make notes
         ns = _construct_unprolated_notes(ps, ds, direction)
         #t = Tuplet(multiplier, ns)
         t = Tuplet(multiplier, ns)
         result.append(t)
   return result
