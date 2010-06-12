from abjad.tools import componenttools
from abjad.tools import mathtools
from abjad.tools.chordtools.cast_defective_chord import cast_defective_chord


def yield_all_subchords_of_chord(chord):
   '''.. versionadded:: 1.1.2

   Yield all subchords of `chord`. 

   * Yield newly constructed Abjad chord instances. 
   * Include "empty chord" as a rest.
   * Include `chord` itself.
   * Yield subchords in binary string order.

   ::

      abjad> chord = Chord([0, 2, 8, 9], (1, 4))
      abjad> for subchord in chordtools.yield_all_subchords_of_chord(chord):
      ...     subchord
      ... 
      Rest(4)
      Note(c', 4)
      Note(d', 4)
      Chord(c' d', 4)
      Note(af', 4)
      Chord(c' af', 4)
      Chord(d' af', 4)
      Chord(c' d' af', 4)
      Note(a', 4)
      Chord(c' a', 4)
      Chord(d' a', 4)
      Chord(c' d' a', 4)
      Chord(af' a', 4)
      Chord(c' af' a', 4)
      Chord(d' af' a', 4)
      Chord(c' d' af' a', 4)

   .. versionchanged:: 1.1.2
      renamed ``chordtools.subchords( )`` to
      ``chordtools.yield_all_subchords_of_chord( )``.
   '''

   len_chord = len(chord)
   for i in range(2 ** len_chord):
      new_chord = componenttools.clone_components_and_remove_all_spanners([chord])[0]
      binary_string = mathtools.binary_string(i)
      binary_string = binary_string.zfill(len_chord)
      for j, digit in enumerate(reversed(binary_string)):
         if digit == '0':
            new_chord[j]._remove_me = True
      for note_head in new_chord.note_heads:
         if getattr(note_head, '_remove_me', False):
            new_chord.remove(note_head)
      new_chord = cast_defective_chord(new_chord)
      yield new_chord
