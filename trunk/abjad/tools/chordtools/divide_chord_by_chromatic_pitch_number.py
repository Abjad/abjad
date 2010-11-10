from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools.chordtools._divide_chord import _divide_chord


def divide_chord_by_chromatic_pitch_number(chord, pitch = NamedChromaticPitch('b', 3)):
   r'''Divide `chord` by chromatic `pitch` number::

      abjad> chord = Chord(range(12), Fraction(1, 4))

   ::

      abjad> chord
      Chord(c' cs' d' ef' e' f' fs' g' af' a' bf' b', 4)

   ::

      abjad> chordtools.divide_chord_by_chromatic_pitch_number(chord, NamedChromaticPitch(6))
      (Chord(fs' g' af' a' bf' b', 4), Chord(c' cs' d' ef' e' f', 4))

   Input `chord` may be a note, rest or chord but not a skip.

   Zero-length parts return rests, length-one parts return notes and
   other parts return chords.

   Return pair of newly constructed leaves.

   .. versionchanged:: 1.1.2
      renamed ``chordtools.split_by_pitch_number( )`` to
      ``chordtools.divide_chord_by_chromatic_pitch_number( )``.
   '''

   treble_chord, bass_chord = _divide_chord(chord, pitch = pitch, attr = 'numbered_chromatic_pitch')

   return treble_chord, bass_chord
