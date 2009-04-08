from abjad.tools import duration
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
   for wd in duration.token_decompose(dur):
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


