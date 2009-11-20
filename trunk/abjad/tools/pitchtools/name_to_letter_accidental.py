def name_to_letter_accidental(name):
   '''Return name, accidental pair corresponding 
   to pitch `name` string. ::

      abjad> pitchtools.name_to_letter_accidental('c')
      ('c', '')
      abjad> pitchtools.name_to_letter_accidental('cs')
      ('c', 's')
      abjad> pitchtools.name_to_letter_accidental('d')
      ('d', '')
      abjad> pitchtools.name_to_letter_accidental('ds')
      ('d', 's')
   '''

   if len(name) == 1:
      return name, ''
   else:
      return name[0], name[1:]
