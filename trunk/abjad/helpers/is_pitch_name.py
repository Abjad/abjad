_diatonic_names = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
_accidental_names = ['', '!', 's', 'f', 'ss', 'ff', 'qs', 'qf', 'tqs', 'tqf']
_pitch_names = [ ]

for _dn in _diatonic_names:
   for _an in _accidental_names:
      _pitch_names.append(_dn + _an)

def _is_pitch_name(arg):
   '''Returns True when arg has the form of a
      LilyPond pitch name in English, otherwise False.'''
   return arg in _pitch_names
