def pc_to_pitch_name_sharps(pc):
   '''Return pitch name string corresponding to `pc` spelled
   with zero or more sharps. ::

      abjad> for n in range(13):
      ...     pc = n / 2.0
      ...     name = pitchtools.pitch_class_number_to_pitch_name_with_flats_sharps(pc)
      ...     print '%s\\t%s' % (pc, name)
      ... 
      0.0   c
      0.5   cqs
      1.0   cs
      1.5   ctqs
      2.0   d
      2.5   dqs
      3.0   ds
      3.5   dtqs
      4.0   e
      4.5   eqs
      5.0   f
      5.5   fqs
      6.0   fs
   '''

   try:
      return _pcToPitchNameSharps[pc]
   except KeyError:
      return _pcToPitchNameSharps[pc.number]


_pcToPitchNameSharps = {
      0:  'c',     0.5: 'cqs',    1: 'cs',    1.5:  'ctqs',
      2:  'd',     2.5: 'dqs',    3: 'ds',    3.5:  'dtqs',
      4:  'e',     4.5: 'eqs',    5: 'f',     5.5:  'fqs',
      6:  'fs',    6.5: 'ftqs',   7: 'g',     7.5:  'gqs',
      8:  'gs',    8.5: 'gtqs',   9: 'a',     9.5:  'aqs',
      10: 'as',   10.5: 'atqs',  11: 'b',    11.5:  'bqs' }
