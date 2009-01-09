from abjad.note.note import Note


def chord_arpeggiate(chord):
   '''
   Return a list of notes equalling the pitches in chord.
   Notes set written duration equal to chord.
   Notes do not inherit articulations, overrides or other chord attributes.
   '''

   result = [ ]
   chord_written_duration = chord.duration.written
   for pitch in chord.pitches:
      result.append(Note(pitch, chord_written_duration))
   return result
