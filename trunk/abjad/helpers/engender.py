from abjad.chord.chord import Chord
from abjad.tools import durtools
from abjad.note.note import Note
from abjad.rest.rest import Rest
from abjad.tools import pitch


def engender(pitches, duration):
   '''Create note, rest or skip from pitches and duration.'''
   assert pitch.is_token_collection(pitches)
   assert durtools.is_token(duration)
   if len(pitches) == 0:
      return Rest(duration)
   elif len(pitches) == 1:
      return Note(tuple(pitches)[0], duration)
   else:
      return Chord(pitches, duration)
