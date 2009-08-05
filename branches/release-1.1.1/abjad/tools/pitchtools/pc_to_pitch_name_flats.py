_pcToPitchNameFlats = {
      0:  'c',     0.5: 'dtqf',    1: 'df',    1.5:  'dqf',
      2:  'd',     2.5: 'etqf',    3: 'ef',    3.5:  'eqf',
      4:  'e',     4.5: 'fqf',     5: 'f',     5.5:  'gtqf',
      6:  'gf',    6.5: 'gqf',     7: 'g',     7.5:  'atqf',
      8:  'af',    8.5: 'aqf',     9: 'a',     9.5:  'btqf',
      10: 'bf',   10.5: 'bqf',    11: 'b',    11.5:  'cqf' }

def pc_to_pitch_name_flats(pc):
   return _pcToPitchNameFlats[pc]
