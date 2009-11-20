def diatonic_interval_to_staff_spaces(diatonic_interval):
   '''Return nonnegative integer number staff spaces corresponding
   to unqualified `diatonic_interval` string. ::

      abjad> pitchtools.diatonic_interval_to_staff_spaces('unison')
      0
      abjad> pitchtools.diatonic_interval_to_staff_spaces('second')
      1
      abjad> pitchtools.diatonic_interval_to_staff_spaces('third')
      2
      abjad> pitchtools.diatonic_interval_to_staff_spaces('fourth')
      3
      abjad> pitchtools.diatonic_interval_to_staff_spaces('fifth')
      4
      abjad> pitchtools.diatonic_interval_to_staff_spaces('sixth')
      5
      abjad> pitchtools.diatonic_interval_to_staff_spaces('seventh')
      6
      abjad> pitchtools.diatonic_interval_to_staff_spaces('octave')
      7
   '''

   return _diatonicIntervalToStaffSpaces[diatonic_interval]


_diatonicIntervalToStaffSpaces = {
   'unison': 0,   'second': 1,   'third': 2,
   'fourth': 3,   'fifth': 4,    'sixth': 5,
   'seventh': 6,  'octave': 7,   'ninth': 8,
   'tenth': 9,    'eleventh': 10, 'twelth': 11,
   'thirteenth': 12 }
