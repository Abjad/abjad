def diatonic_interval_string_to_diatonic_interval_number(
   diatonic_interval_string):
   r'''.. versionadded:: 1.1.2

   Return diatonic interval number corresponding to
   `diatonic_interval_string`. ::

      abjad> pitchtools.diatonic_interval_string_to_diatonic_interval_number('unison')
      1
      abjad> pitchtools.diatonic_interval_string_to_diatonic_interval_number('second') 
      2
      abjad> pitchtools.diatonic_interval_string_to_diatonic_interval_number('third')
      3
      abjad> pitchtools.diatonic_interval_string_to_diatonic_interval_number('fourth') 
      4
      abjad> pitchtools.diatonic_interval_string_to_diatonic_interval_number('fifth')
      5
   '''

   return _diatonic_interval_string_to_diatonic_interval_number[
      diatonic_interval_string]

      
_diatonic_interval_string_to_diatonic_interval_number = {
   'unison': 1, 'second': 2, 'third': 3,
   'fourth': 4, 'fifth': 5, 'sixth': 6,
   'seventh': 7, 'octave': 8, 'ninth': 9,
   'tenth': 10, 'eleventh': 11, 'twelth': 12,}
