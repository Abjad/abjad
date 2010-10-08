def apply_accidental_to_named_chromatic_pitch(named_chromatic_pitch, accidental = None):
   '''Apply `accidental` to `named_chromatic_pitch`.

   Return new named pitch.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.apply_accidental_to_named_chromatic_pitch( )`` to
      ``pitchtools.apply_accidental_to_named_chromatic_pitch( )``.
   '''

   from abjad.tools.pitchtools.Accidental import Accidental
   accidental = Accidental(accidental)
   new_accidental = named_chromatic_pitch.accidental + accidental
   new_name = named_chromatic_pitch.diatonic_pitch_class_name + new_accidental.alphabetic_string
   return type(named_chromatic_pitch)(new_name, named_chromatic_pitch.octave_number)
