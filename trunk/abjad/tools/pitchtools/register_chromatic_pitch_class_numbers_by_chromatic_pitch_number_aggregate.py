from abjad.tools import seqtools


def register_chromatic_pitch_class_numbers_by_chromatic_pitch_number_aggregate(pcs, pitches):
   '''Turn numeric `pcs` into numeric `pitches`.
   
   ::

      abjad> pitchtools.register_chromatic_pitch_class_numbers_by_chromatic_pitch_number_aggregate(
      ...     [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11],
      ...     [10, 19, 20, 23, 24, 26, 27, 29, 30, 33, 37, 40])
      [10, 24, 26, 30, 20, 19, 29, 27, 37, 33, 40, 23]

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.registrate( )`` to
      ``pitchtools.register_chromatic_pitch_class_numbers_by_chromatic_pitch_number_aggregate( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.register_pitch_class_numbers_by_pitch_number_aggregate( )`` to
      ``pitchtools.register_chromatic_pitch_class_numbers_by_chromatic_pitch_number_aggregate( )``.
   '''

   if isinstance(pcs, list):
      r = [[p for p in pitches if p % 12 == pc] for pc in [x % 12 for x in pcs]]
      r = seqtools.flatten_sequence(r)
   elif isinstance(pcs, int):
      r = [p for p in pitches if p % 12 == pcs][0]
   else:
      raise TypeError

   return r
