_diatonic_pitch_class_name_to_diatonic_pitch_class_number = {
   'c': 0, 'd': 1, 'e': 2, 'f': 3, 'g': 4, 'a': 5, 'b': 6 }


def diatonic_pitch_class_name_to_diatonic_pitch_class_number(diatonic_pitch_class_name):
   '''Get diatonic pitch-class number from `diatonic_pitch_class_name`:

   ::
      abjad> pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number('c')
      0
   '''
   
   try:
      return _diatonic_pitch_class_name_to_diatonic_pitch_class_number[diatonic_pitch_class_name]
   except KeyError:
      return None
