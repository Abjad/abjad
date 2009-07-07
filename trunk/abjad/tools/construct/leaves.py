from __future__ import division
from abjad.rational import Rational
from abjad.tools import durtools
from abjad.tools import listtools
from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools.construct._construct_tied_chord import _construct_tied_chord
from abjad.tools.construct._construct_tied_note import _construct_tied_note
from abjad.tools.construct._construct_tied_rest import _construct_tied_rest
from abjad.tuplet import FixedMultiplierTuplet


## TODO: Change construct.leaves( ) signature to allow ('c', 4) named pairs 
##       This will allow the creation of enharmonic equivalents.
##       Examples: construct.leaves([('c', 4), ('cs', 4)], [(1, 4)])

## TODO: Extend construct.leaves( ) to accept Abjad Pitch instances. Ex:
##       Example: construct.leaves([Pitch('cs', 4)], [(1, 4)])

## TODO: Deprecate construct.engender( ) in favor of construct.leaves( );
##       Only possible after the two extensions to construct.leaves( ), above.

def leaves(pitches, durations, direction='big-endian', tied_rests=False):
   '''Constructs a list of prolated and/or unprolated leaves of length 
      len(durations).
      The type of the leaves returned depends on the type of the pitches given.
      Integer pitches create Notes.
      Tuple pitches create Chords.
      None pitches create Rests.
      e.g. pitches = [12, (1,2,3), None, 12]
      Will create a Note with pitch 12, a Chord with pitches (1,2,3), a
      Rest and another Note with pitch 12.


      * `pitches` is a single pitch or a list/tuple of pitches. If the list is
         smaller than that of the durations, the pitches are cycled through.

      * `durations` is a sinlge duration or a list of durations. The durations
         need not be of form m / 2**n and may be any rational value.

      * `direction` may be 'big-endian' or 'little-endian'.
         'big-endian' returns list of notes of decreasing duration.
         'little-endian' returns list of notes of increasing duration.

      * `tied_rests`: Set to True to return Tied rests. False otherwise.
   '''

   def _make_leaf_on_pitch(pch, ds, direction):
      if isinstance(pch, (int, long)):
         leaves = _construct_tied_note(pch, ds, direction)
      elif isinstance(pch, (tuple, list)):
         leaves = _construct_tied_chord(pch, ds, direction)
      elif pch is None:
         leaves = _construct_tied_rest(ds, direction, tied_rests)
      else:
         raise ValueError("Unknown pitch token %s." % pch)
      return leaves

   if pitchtools.is_token(pitches):
      pitches = [pitches]
   
   if durtools.is_token(durations):
      durations = [durations]

   ## convert Rationals to duration tokens.
   durations = [durtools.token_unpack(dur) for dur in durations]

   ## set lists of pitches and durations to the same length
   size = max(len(durations), len(pitches))
   #durations = listtools.resize(durations, size)
   #pitches = listtools.resize(pitches, size)
   durations = listtools.repeat_list_to_length(durations, size)
   pitches = listtools.repeat_list_to_length(pitches, size)

   durations = durtools.agglomerate_by_prolation(durations)

   result = [ ]
   for ds in durations:
      ## get factors in denominator of duration group ds other than 1, 2.
      factors = set(mathtools.factors(ds[0][1]))
      factors.discard(1)
      factors.discard(2)
      ps = pitches[0:len(ds)]
      pitches = pitches[len(ds):]
      if len(factors) == 0:
         for pch, dur in zip(ps, ds):
            leaves = _make_leaf_on_pitch(pch, dur, direction)
            result.extend(leaves)
      else:
         ## compute prolation
         denominator = ds[0][1]
         numerator = mathtools.greatest_power_of_two_less_equal(denominator)
         multiplier = (numerator, denominator)
         ratio = 1 / Rational(*multiplier)
         ds = [ratio * Rational(*d) for d in ds]
         ## make leaves
         leaves = [ ]
         for pch, dur in zip(ps, ds):
            leaves.extend( _make_leaf_on_pitch(pch, dur, direction))
         t = FixedMultiplierTuplet(multiplier, leaves)
         result.append(t)
   return result
