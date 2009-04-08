from abjad.helpers.duration_token_unpack import _duration_token_unpack
from abjad.rational.rational import Rational
from abjad.tools.construct.helpers import _construct_tied_note, \
   _construct_tied_rest


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
