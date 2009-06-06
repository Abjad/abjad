from abjad.chord.chord import Chord
from abjad.note.note import Note


def arpeggiate(chord):
   '''Return a Python list of newly-instantiated Abjad Note instances 
   derived from the pitches in *chord*.

   *  ``chord`` must be an Abjad Chord instance.
   *  ``note.duration.written == chord.duration.written`` for every \
      ``note`` in ``result``.
   *  notes inherit neither articulations, overrides nor any of the \
      other attributes of *chord*.'''
   
   assert isinstance(chord, Chord)

   result = [ ]
   chord_written_duration = chord.duration.written
   for pitch in chord.pitches:
      result.append(Note(pitch, chord_written_duration))

   return result
