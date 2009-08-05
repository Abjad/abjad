def pc_to_pitch_name(pc):
   return _pcToPitchName[pc]
   

_pcToPitchName = {
   0:  'c',     0.5: 'cqs',    1: 'cs',    1.5:  'dqf',
   2:  'd',     2.5: 'dqs',    3: 'ef',    3.5:  'eqf',
   4:  'e',     4.5: 'eqs',    5: 'f',     5.5:  'fqs',
   6:  'fs',    6.5: 'gqf',    7: 'g',     7.5:  'gqs',
   8:  'af',    8.5: 'aqf',    9: 'a',     9.5:  'aqs',
   10: 'bf',   10.5: 'bqf',   11: 'b',    11.5:  'bqs' }
