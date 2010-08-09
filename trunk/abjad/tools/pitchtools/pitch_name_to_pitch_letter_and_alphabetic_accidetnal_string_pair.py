def pitch_name_to_pitch_letter_and_alphabetic_accidetnal_string_pair(name):
   '''Return name, accidental pair corresponding 
   to pitch `name` string. ::

      abjad> pitchtools.pitch_name_to_pitch_letter_and_alphabetic_accidetnal_string_pair('c')
      ('c', '')
      abjad> pitchtools.pitch_name_to_pitch_letter_and_alphabetic_accidetnal_string_pair('cs')
      ('c', 's')
      abjad> pitchtools.pitch_name_to_pitch_letter_and_alphabetic_accidetnal_string_pair('d')
      ('d', '')
      abjad> pitchtools.pitch_name_to_pitch_letter_and_alphabetic_accidetnal_string_pair('ds')
      ('d', 's')

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.name_to_letter_accidental( )`` to
      ``pitchtools.pitch_name_to_pitch_letter_and_alphabetic_accidetnal_string_pair( )``.
   '''

   if len(name) == 1:
      return name, ''
   else:
      return name[0], name[1:]
