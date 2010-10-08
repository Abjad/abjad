def chromatic_pitch_class_name_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_pair(name):
   '''Return name, accidental pair corresponding 
   to pitch `name` string. ::

      abjad> pitchtools.chromatic_pitch_class_name_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_pair('c')
      ('c', '')
      abjad> pitchtools.chromatic_pitch_class_name_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_pair('cs')
      ('c', 's')
      abjad> pitchtools.chromatic_pitch_class_name_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_pair('d')
      ('d', '')
      abjad> pitchtools.chromatic_pitch_class_name_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_pair('ds')
      ('d', 's')

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.name_to_letter_accidental( )`` to
      ``pitchtools.chromatic_pitch_class_name_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_pair( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.pitch_name_to_pitch_letter_and_alphabetic_accidetnal_string_pair( )`` to
      ``pitchtools.chromatic_pitch_class_name_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_pair( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.chromatic_pitch_class_name_to_diatonic_pitch_class_name_alphabetic_accidental_string_pair( )`` to
      ``pitchtools.chromatic_pitch_class_name_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_pair( )``.
   '''

   if len(name) == 1:
      return name, ''
   else:
      return name[0], name[1:]
