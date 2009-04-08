from __future__ import division
from abjad.helpers.agglomerate_durations_by_prolation import \
     _agglomerate_durations_by_prolation
from abjad.tools import duration
from abjad.helpers.is_pitch_token import is_pitch_token
from abjad.helpers.is_duration_token import _is_duration_token
from abjad.tools import mathtools
from abjad.helpers.resize_list import _resize_list
from abjad.rational.rational import Rational
from abjad.tools.construct.helpers import _construct_tied_chord, \
   _construct_tied_note, _construct_tied_rest
from abjad.tools import mathtools
from abjad.tuplet.fm.tuplet import FixedMultiplierTuplet


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

      Parameters:
      pitches:    a single pitch or a list/tuple of pitches. If the list is
                  smaller than that of the durations, the pitches are cycled 
                  through.
      durations:  a sinlge duration or a list of durations. The durations
                  need not be of form m / 2**n and may be any rational value.
      direction:  may be 'big-endian' or 'little-endian'.
                  'big-endian' returns list of notes of decreasing duration.
                  'little-endian' returns list of notes of increasing duration.
      tied_rests: Set to True to return Tied rests. False otherwise.
   '''

   def _make_leaf_on_pitch(pitch, ds, direction):
      if isinstance(pitch, (int, long)):
         leaves = _construct_tied_note(pitch, ds, direction)
      elif isinstance(pitch, (tuple, list)):
         leaves = _construct_tied_chord(pitch, ds, direction)
      elif pitch is None:
         leaves = _construct_tied_rest(ds, direction, tied_rests)
      else:
         raise ValueError("Unknown pitch token %s." % pitch)
      return leaves

   if is_pitch_token(pitches):
      pitches = [pitches]
   
   if _is_duration_token(durations):
      durations = [durations]

   ## convert Rationals to duration tokens.
   durations = [duration.token_unpack(dur) for dur in durations]

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
         for pitch, dur in zip(ps, ds):
            leaves = _make_leaf_on_pitch(pitch, dur, direction)
            result.extend(leaves)
      else:
         ## compute prolation
         denominator = ds[0][1]
         numerator = mathtools.next_least_power_of_two(denominator)
         multiplier = (numerator, denominator)
         ratio = 1 / Rational(*multiplier)
         ds = [ratio * Rational(*d) for d in ds]
         ## make leaves
         leaves = [ ]
         for pitch, dur in zip(ps, ds):
            leaves.extend( _make_leaf_on_pitch(pitch, dur, direction))
         t = FixedMultiplierTuplet(multiplier, leaves)
         result.append(t)
   return result
