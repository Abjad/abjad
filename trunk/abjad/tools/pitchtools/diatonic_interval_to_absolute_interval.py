def diatonic_interval_to_absolute_interval(interval):
   _diatonicIntervalToAbsoluteInterval = {
      'perfect unison': 0, 'minor second': 1, 'major second': 2,
      'minor third': 3, 'major third': 4, 'perfect fourth': 5,
      'augmented fourth': 6, 'diminished fifth': 6, 'perfect fifth': 7,
      'minor sixth': 8, 'major sixth': 9, 'minor seventh': 10,
      'major seventh': 11, 'perfect octave': 12 }
   return _diatonicIntervalToAbsoluteInterval[interval]
