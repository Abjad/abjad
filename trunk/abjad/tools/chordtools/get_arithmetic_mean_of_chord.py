def get_arithmetic_mean_of_chord(chord):
   '''Return arithmetic mean of pitch numbers in chord::

      abjad> chord = Chord([7, 12, 16], (1, 4))
      abjad> chordtools.get_arithmetic_mean_of_chord(chord)
      11.666666666666666

   Return none when chord is emtpy::

      abjad> chord = Chord([ ], (1, 4))
      abjad> chordtools.get_arithmetic_mean_of_chord(chord) is None
      True

   This function externalizes the `center` attribute previously bound to chords.
   '''

   numbers = [ ]
   for pitch in chord.pitches:
      numbers.append(pitch.pitch_number)
   if numbers:
      return sum(numbers).__truediv__(len(numbers))
   else:
      return None
