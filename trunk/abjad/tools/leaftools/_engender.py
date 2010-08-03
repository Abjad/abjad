from abjad.components.Chord import Chord
from abjad.components.Note import Note
from abjad.components.Rest import Rest
from abjad.tools import durtools
from abjad.tools import pitchtools


def _engender(pitches, duration):
   '''Create note, rest or skip from pitches and duration.

   .. todo:: deprecate ``construct.engender( )`` in favor of
      ``construct.leaves( )``.
   '''

   assert pitchtools.is_pitch_token_collection(pitches)
   assert durtools.is_duration_token(duration)
   if len(pitches) == 0:
      return Rest(duration)
   elif len(pitches) == 1:
      return Note(tuple(pitches)[0], duration)
   else:
      return Chord(pitches, duration)
