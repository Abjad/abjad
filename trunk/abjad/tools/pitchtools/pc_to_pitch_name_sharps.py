_pcToPitchNameSharps = {
      0:  'c',     0.5: 'cqs',    1: 'cs',    1.5:  'ctqs',
      2:  'd',     2.5: 'dqs',    3: 'ds',    3.5:  'dtqs',
      4:  'e',     4.5: 'eqs',    5: 'f',     5.5:  'fqs',
      6:  'fs',    6.5: 'ftqs',   7: 'g',     7.5:  'gqs',
      8:  'gs',    8.5: 'gtqs',   9: 'a',     9.5:  'aqs',
      10: 'as',   10.5: 'atqs',  11: 'b',    11.5:  'bqs' }

def pc_to_pitch_name_sharps(pc):
   return _pcToPitchNameSharps[pc]
