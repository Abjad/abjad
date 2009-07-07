from abjad.rational import Rational
from abjad.rest import Rest
from abjad.note import Note
from abjad.tools import durtools
from abjad.tools.construct._construct_tied_note import _construct_tied_note
from abjad.tools.construct._construct_tied_rest import  _construct_tied_rest
from abjad.tools.construct._construct_tied_leaf import  _construct_tied_leaf


def percussion_note(pitch, total_duration, max_note_duration=(1, 8)):
   '''Returns a list containing a single Note and possibly a succession
   of Rests, depending on the values given to the duration arguments.
   The duration of the note returned is always smaller or equal to 
   *max_note_duration*. The total duration of the rests returned is 
   the difference between *total_duration* and the duration of the 
   note returned. Rests are used to pad the duration of the note to fit
   the *total_duration* if the *total_duration* will result in tied Notes. 
   Useful for percussion music where the duration of the attack is 
   negligible and you don't want tied notes.

   * `pitch` can be any *pitch token*.
   * `total_duration` is the duration resulting from the sum of the \
      durations of the objects returned.
   * `max_note_duration` is the maximum duration that the note returned \
      will have.


   Examples:
   
   ::

      abjad> percussion_note(2, (1, 4), (1, 8))
      [Note(d', 8), Rest(8)]

      abjad> percussion_note(2, (1, 64), (1, 8))
      [Note(d', 64)]

      abjad> percussion_note(2, (5, 64), (1, 8))
      [Note(d', 16), Rest(64)]

      abjad> percussion_note(2, (5, 4), (1, 8))
      [Note(d', 8), Rest(1), Rest(8)]
   '''

   total_duration = Rational(*durtools.token_unpack(total_duration))
   max_note_duration = Rational(*durtools.token_unpack(max_note_duration))

   if total_duration > max_note_duration:
      rest_duration = total_duration - max_note_duration
      r = _construct_tied_rest(rest_duration)
      n = _construct_tied_note(pitch, max_note_duration)
   else:
      #n = _construct_tied_note(pitch, total_duration)
      n = _construct_tied_leaf(Note, total_duration, 
         pitches = pitch, tied = False)
      if len(n) > 1:
         for i in range(1, len(n)):
            n[i] = Rest(n[i])
      r = [ ]
   return n + r
