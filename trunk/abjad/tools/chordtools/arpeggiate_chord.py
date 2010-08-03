from abjad.components.Chord import Chord
from abjad.components.Note import Note


def arpeggiate_chord(chord):
   '''Return a list of newly-instantiated notes
   derived from the pitches in `chord`. 

   Arpeggiated notes carry the same written duration as the chord
   from which they derive. ::

      abjad> chord = Chord([0, 14, 15], (3, 16))
      abjad> chordtools.arpeggiate_chord(chord)
      [Note(c', 8.), Note(d'', 8.), Note(ef'', 8.)]

   Arpeggiated notes inherit neither articulations,
   overrides nor any of the other attributes of the chord from
   which they derive. ::

      abjad> chord = Chord([0, 14, 15], (3, 16))
      abjad> chord.articulations.append('staccato')
      abjad> f(chord)
      <c' d'' ef''>8. -\staccato

   ::

      abjad> notes = chordtools.arpeggiate_chord(chord)
      abjad> notes
      [Note(c', 8.), Note(d'', 8.), Note(ef'', 8.)]
      abjad> f(notes[0])
      c'8.

   .. versionchanged:: 1.1.2
      renamed ``chordtools.arpeggiate( )`` to
      ``chordtools.arpeggiate_chord( )``.
   '''
   
   assert isinstance(chord, Chord)

   result = [ ]
   chord_written_duration = chord.duration.written
   for pitch in chord.pitches:
      result.append(Note(pitch, chord_written_duration))

   return result
