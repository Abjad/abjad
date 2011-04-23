def get_arithmetic_mean_of_chord(chord):
   '''.. versionadded:: 1.1.2

   Get arithmetic mean of chromatic pitch number of pitches in `chord`::

      abjad> chord = Chord("<g' c'' e''>4")

   ::

      abjad> chordtools.get_arithmetic_mean_of_chord(chord)
      11.666666666666666

   Return none when `chord` is empty::

      abjad> chord = Chord("< >4")

   ::

      abjad> chordtools.get_arithmetic_mean_of_chord(chord) is None
      True

   Return number or none.
   '''

   numbers = [ ]
   for pitch in chord.pitches:
      numbers.append(pitch.numbered_chromatic_pitch._chromatic_pitch_number)
   if numbers:
      return sum(numbers).__truediv__(len(numbers))
   else:
      return None
