def ordered_chromatic_pitch_class_numbers_are_within_ordered_chromatic_pitch_numbers(pcs, pitches):
   '''True if `pcs` all appear
   in octave-relative order in `pitches`. ::

      abjad> pcs = [2, 7, 10]
      abjad> pitches = [6, 9, 12, 13, 14, 19, 22, 27, 28, 29, 32, 35]
      abjad> pitchtools.ordered_chromatic_pitch_class_numbers_are_within_ordered_chromatic_pitch_numbers(pcs, pitches)
      True

   .. todo:: extend ``pitchtools.ordered_chromatic_pitch_class_numbers_are_within_ordered_chromatic_pitch_numbers( )`` to work on 
      Abjad pitch instances.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.are_in_octave_order( )`` to
      ``pitchtools.ordered_chromatic_pitch_class_numbers_are_within_ordered_chromatic_pitch_numbers( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.ordered_pitch_class_numbers_are_within_ordered_pitch_numbers( )`` to
      ``pitchtools.ordered_chromatic_pitch_class_numbers_are_within_ordered_chromatic_pitch_numbers( )``.
   '''

   pcsStartIndex = [p % 12 for p in pitches].index(pcs[0] % 12)
   pcsTransposition = pitches[pcsStartIndex] - pcs[0]
   transposedPCs = [p + pcsTransposition for p in pcs]
   return set(transposedPCs).issubset(set(pitches))
