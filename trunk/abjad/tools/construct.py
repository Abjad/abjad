from __future__ import division
from abjad.helpers.duration_token_decompose import _duration_token_decompose
from abjad.helpers.is_duration_token import _is_duration_token
from abjad.helpers.is_pitch_token import is_pitch_token
from abjad.chord.chord import Chord
from abjad.note.note import Note
from abjad.rest.rest import Rest
from abjad.tie.spanner import Tie


def _construct_tied_leaf(kind, dur, direction='big-endian', pitches=None,
      tied=True):
   '''Returns a list of Leaves to fill the given duration. 
      Leaves returned are Tie spanned.
      dur:  must be of the form m / 2**n for any m integer.
      direction: may be 'big-endian' or 'little-endian'.
            'big-endian' returns a list of notes of decreasing duration.
            'little-endian' returns a list of notes of increasing duration.
      pitches: a pitch or list of pitch tokens.
      tied: True to return tied leaves, False otherwise. Defaults to True.'''

   result = [ ]
   for wd in _duration_token_decompose(dur):
      if not pitches is None:
         args = (pitches, wd)
      else:
         args = (wd, )
      result.append( kind(*args) )
   if len(result) > 1:
      if direction == 'little-endian':
         result.reverse( )
      if tied:
         Tie(result)
   return result


def _construct_tied_chord(pitches, dur, direction='big-endian'):
   '''Returns a list of chords to fill the given duration. 
      Chords returned are Tie spanned.'''
   return _construct_tied_leaf(Chord, dur, direction, pitches)


def _construct_tied_rest(dur, direction='big-endian', tied=False):
   '''Returns a list of rests to fill given duration. 
      Rests returned are Tie spanned.'''
   return _construct_tied_leaf(Rest, dur, direction, None, tied)


def _construct_tied_note(pitch, dur, direction='big-endian'):
   '''Returns a list of notes to fill the given duration. 
      Notes returned are Tie spanned.'''
   return _construct_tied_leaf(Note, dur, direction, pitch)


def _construct_unprolated_notes(pitches, durations, direction='big-endian'):
   '''Private helper returns a list of unprolated notes.'''
   assert len(pitches) == len(durations)
   result = [ ]
   for pitch, dur in zip(pitches, durations):
      result.extend(_construct_tied_note(pitch, dur, direction))
   return result


def rests(durations, direction='big-endian', tied=False):
   '''Constructs a list of rests.
      Parameters:
      durations:  a sinlge duration or a list of durations.
      direction:  may be 'big-endian' or 'little-endian'.
            'big-endian' returns a list of notes of decreasing duration.
            'little-endian' returns a list of notes of increasing duration.
      tied: Set to True to return tied rests. False otherwise.  '''

   if _is_duration_token(durations):
      durations = [durations]

   result = [ ]
   for d in durations:
      result.extend(_construct_tied_rest(d, direction, tied))
   return result


from abjad.helpers.duration_token_unpack import _duration_token_unpack
from abjad.rational.rational import Rational

def percussion_note(pitch, total_duration, max_note_duration=(1, 8)):
   '''Returns a list containing a single Note and a succession or Rests.
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
      [Note(d', 8), Rest(1), Rest(8)]'''

   total_duration = Rational(*_duration_token_unpack(total_duration))
   max_note_duration = Rational(*_duration_token_unpack(max_note_duration))
   if total_duration > max_note_duration:
      rest_duration = total_duration - max_note_duration
      r = _construct_tied_rest(rest_duration)
      n = _construct_tied_note(pitch, max_note_duration)
   else:
      n = _construct_tied_note(pitch, total_duration)
      if len(n) > 1:
         for i in range(1, len(n)):
            n[i] = Rest(n[i])
      r = [ ]
   return n + r


from abjad.helpers.agglomerate_durations_by_prolation import \
     _agglomerate_durations_by_prolation
from abjad.helpers.resize_list import _resize_list
from abjad.helpers.next_least_power_of_two import _next_least_power_of_two
from abjad.tuplet.fm.tuplet import FixedMultiplierTuplet
from abjad.tools import mathtools
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
      #result.extend(notes_prolated(pitch, [multiplied_remainder]))
      result.extend(notes(pitch, [multiplied_remainder]))
   return result


from abjad.tools import interpolate

def notes_curve(pitches, total, start, stop, exp='cosine', 
   written=Rational(1, 8)):
   '''Returns a train of notes with 'continuously' changing effective durations
      given as the written duration argument times the computed interpolated 
      multipliers. The default written duration is 1/8 note.
      The durations are interpolated from start duration
      argument to stop duration argument. 
      The function returns as many interpolation values as necessary to 
      fill the total duration requested.
      The pitches of the notes are set cyclically from the pitches list.'''

   total = Rational(*_duration_token_unpack(total))
   start = Rational(*_duration_token_unpack(start))
   stop = Rational(*_duration_token_unpack(stop))
   written = Rational(*_duration_token_unpack(written))

   dts = interpolate.divide(total, start, stop, exp)
   result = [ ]
   for i, dt in enumerate(dts):
      note = Note(pitches[i % len(pitches)], written)
      note.duration.multiplier = dt / written 
      result.append(note)
   return result
   

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
         for pitch, dur in zip(ps, ds):
            leaves = _make_leaf_on_pitch(pitch, dur, direction)
            result.extend(leaves)
      else:
         ## compute prolation
         denominator = ds[0][1]
         numerator = _next_least_power_of_two(denominator)
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
