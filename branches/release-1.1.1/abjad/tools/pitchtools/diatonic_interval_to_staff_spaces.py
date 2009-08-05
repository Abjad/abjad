def diatonic_interval_to_staff_spaces(interval):
   _diatonicIntervalToStaffSpaces = {
      'unison': 0,   'second': 1,   'third': 2,
      'fourth': 3,   'fifth': 4,    'sixth': 5,
      'seventh': 6,  'octave': 7,   'ninth': 8,
      'tenth': 9,    'eleventh': 10, 'twelth': 11,
      'thirteenth': 12 }
   return _diatonicIntervalToStaffSpaces[interval]
