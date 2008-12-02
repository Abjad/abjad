from abjad.chord.chord import Chord
from abjad.helpers.is_duration_token import _is_duration_token
from abjad.helpers.is_pitch_token_collection import _is_pitch_token_collection
from abjad.note.note import Note
from abjad.rest.rest import Rest


def engender(pitches, duration):
   '''Create note, rest or skip from pitches and duration.'''
   assert _is_pitch_token_collection(pitches)
   assert _is_duration_token(duration)
   if len(pitches) == 0:
      return Rest(duration)
   elif len(pitches) == 1:
      return Note(tuple(pitches)[0], duration)
   else:
      return Chord(pitches, duration)
