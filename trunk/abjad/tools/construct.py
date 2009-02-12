from __future__ import division
from abjad.helpers.duration_token_decompose import _duration_token_decompose
from abjad.helpers.is_duration_token import _is_duration_token
from abjad.helpers.is_pitch_token import _is_pitch_token
from abjad.note.note import Note
from abjad.rest.rest import Rest
from abjad.tie.spanner import Tie


def _construct_rest(dur, direction='big-endian'):
   '''
   Returns a list of rests to fill given duration. 
   Rests returned are Tie spanned. 
   '''
   result = [ ]
   for wd in _duration_token_decompose(dur):
      result.append( Rest(wd) )
   if len(result) > 1:
      if direction == 'little-endian':
         result.reverse( )
      Tie(result)
   return result


def _construct_note(pitch, dur, direction='big-endian'):
   '''
   Returns a list of notes to fill the given duration. 
   Notes returned are Tie spanned.
   direction: may be 'big-endian' or 'little-endian'.
            'big-endian' returns a list of notes of decreasing duration.
            'little-endian' returns a list of notes of increasing duration.
   '''
   result = [ ]
   for wd in _duration_token_decompose(dur):
      result.append(Note(pitch, wd))
   if len(result) > 1:
      if direction == 'little-endian':
         result.reverse( )
      Tie(result)
   return result


from abjad.helpers.duration_token_unpack import _duration_token_unpack

def notes(pitches, durations, direction='big-endian'):
   '''
   Constructs a list of notes of length max(len(pitches), len(durations)).
   The pitches or the durations, whichever is shorter, are cycled around until
   the max length is reached.

   Parameters:
   pitches:    a single pitch or a list/tuple of pitches.
   durations:  a sinlge duration or a list of durations.
   direction:     may be 'big-endian' or 'little-endian'.
               'big-endian' returns a list of notes of decreasing duration.
               'little-endian' returns a list of notes of increasing duration.
   '''

   if _is_pitch_token(pitches):
      pitches = [pitches]

   if _is_duration_token(durations):
      durations = [durations]

   result = [ ]
   max_len = max(len(pitches), len(durations))
   for i in range(max_len):
      d = durations[i % len(durations)]
      d = _duration_token_unpack(d)
      p = pitches[i % len(pitches)]
      result.extend(_construct_note(p, d, direction))
   return result


def rests(durations, direction='big-endian'):
   '''
   Constructs a list of rests.
   Parameters:
   durations:  a sinlge duration or a list of durations.
   direction:  may be 'big-endian' or 'little-endian'.
               'big-endian' returns a list of notes of decreasing duration.
               'little-endian' returns a list of notes of increasing duration.
   '''
   if _is_duration_token(durations):
      durations = [durations]

   result = [ ]
   for d in durations:
      d = _duration_token_unpack(d)
      result.extend(_construct_rest(d, direction))
   return result


from abjad.rational.rational import Rational

def percussion_note(pitch, total_duration, max_note_duration=(1, 8)):
   '''
   Returns a list containing a single Note and a succession or Rests.
   The total duration of the Rests is the difference of the total_duration
   and the max_note_duration if total_duration > max_note_duration.

   Example:
   >>> percussion_note(2, (1, 4), (1, 8))
   [Note(d', 8), Rest(8)]

   >>> percussion_note(2, (1, 64), (1, 8))
   [Note(d', 64)]

   >>> percussion_note(2, (5, 64), (1, 8))
   [Note(d', 16), Rest(64)]

   >>> percussion_note(2, (5, 4), (1, 8))
   [Note(d', 8), Rest(1), Rest(8)]

   '''
   total_duration = Rational(*_duration_token_unpack(total_duration))
   max_note_duration = Rational(*_duration_token_unpack(max_note_duration))
   if total_duration > max_note_duration:
      rest_duration = total_duration - max_note_duration
      r = _construct_rest(rest_duration)
      n = _construct_note(pitch, max_note_duration)
   else:
      n = _construct_note(pitch, total_duration)
      if len(n) > 1:
         for i in range(1, len(n)):
            n[i] = Rest(n[i])
      r = [ ]
   return n + r


from abjad.helpers.agglomerate_durations_by_prolation import \
     _agglomerate_durations_by_prolation
from abjad.helpers.next_least_power_of_two import _next_least_power_of_two
from abjad.helpers.factors import _factors
from abjad.tuplet.fm.tuplet import FixedMultiplierTuplet
import operator
import math
      
def notes_prolated(pitches, durations, direction='big-endian'):
   '''
   Constructs a list of prolated notes of length len(durations).

   Parameters:
   pitches:    a single pitch or a list/tuple of pitches. If the list is
               smaller than that of the durations, the pitches are cycled 
               through.
   durations:  a sinlge duration or a list of durations. The durations
               need not be of the form m / 2**n and may be any rational value.
   direction:  may be 'big-endian' or 'little-endian'.
               'big-endian' returns a list of notes of decreasing duration.
               'little-endian' returns a list of notes of increasing duration.
   '''

   if _is_pitch_token(pitches):
      pitches = [pitches]
   
   if _is_duration_token(durations):
      durations = [durations]

   # this block is a hack to allow the function to accept a Rational
   # as the duration input parameter; better will be to change
   # the rest of the implementation to allow for Rationals directly.

   temp = [ ]
   for duration in durations:
      if isinstance(duration, Rational):
         temp.append((duration._n, duration._d))
      else:
         temp.append(duration)
   durations = temp

   pitches = pitches * int(math.ceil(len(durations) / len(pitches)))
   durations = _agglomerate_durations_by_prolation(durations)

   result = [ ]
   for ds in durations:
      factors = set(_factors(ds[0][1]))
      factors.discard(2)
      ps = pitches[0:len(ds)]
      pitches = pitches[len(ds):]
      if len(factors) == 0:
         result.extend(notes(ps, ds, direction))
      else:
         denominator = reduce(operator.mul, factors)
         numerator = _next_least_power_of_two(denominator)
         #print numerator, denominator
         multiplier = (numerator, denominator)
         ratio = 1 / Rational(*multiplier)
         ds = [ratio * Rational(*d) for d in ds]
         #print ds
         ns = notes(ps, ds, direction)
         #print ns
         t = FixedMultiplierTuplet(multiplier, ns)
         result.append(t)
   return result
      

def note_train(pitch, written_duration, total_duration, 
   prolation = Rational(1)):
   '''Generate a train of repeating notes, all of the same pitch,
      equal to total duration total_duration,
      each with written duration equal to written_duration,
      under prolation context equal to prolation.
      Fill any remaining duration at the end of the train
      with a series of notes with smaller written duration.
      Set prolation when constructing a note train within
      a nonbinary measure.'''

   prolated_duration = prolation * written_duration 
   current_duration = Rational(0)
   result = [ ]
   while current_duration + prolated_duration <= total_duration:
      result.append(Note(pitch, written_duration))
      current_duration += prolated_duration
   remainder_duration = total_duration - current_duration
   if remainder_duration > Rational(0):
      multiplied_remainder = ~prolation * remainder_duration
      result.extend(notes_prolated(pitch, [multiplied_remainder]))
   return result
