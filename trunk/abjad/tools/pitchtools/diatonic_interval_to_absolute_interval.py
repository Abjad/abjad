def diatonic_interval_to_absolute_interval(diatonic_interval):
   '''Return chromatic interval integer corresponding to
   `diatonic_interval` string. ::

      abjad> pitchtools.diatonic_interval_to_absolute_interval('perfect unison')
      0
      abjad> pitchtools.diatonic_interval_to_absolute_interval('minor second')
      1
      abjad> pitchtools.diatonic_interval_to_absolute_interval('major second')
      2
      abjad> pitchtools.diatonic_interval_to_absolute_interval('minor third')
      3
      abjad> pitchtools.diatonic_interval_to_absolute_interval('major third')
      4
      abjad> pitchtools.diatonic_interval_to_absolute_interval('perfect fourth')
      5
      abjad> pitchtools.diatonic_interval_to_absolute_interval('augmented fourth')
      6
      abjad> pitchtools.diatonic_interval_to_absolute_interval('diminished fifth')
      6
      abjad> pitchtools.diatonic_interval_to_absolute_interval('perfect fifth')
      7
   '''

   return _diatonicIntervalToAbsoluteInterval[diatonic_interval]


_diatonicIntervalToAbsoluteInterval = {
   'perfect unison': 0, 'minor second': 1, 'major second': 2,
   'minor third': 3, 'major third': 4, 'perfect fourth': 5,
   'augmented fourth': 6, 'diminished fifth': 6, 'perfect fifth': 7,
   'minor sixth': 8, 'major sixth': 9, 'minor seventh': 10,
   'major seventh': 11, 'perfect octave': 12 }
