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
      print d
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


