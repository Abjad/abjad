def is_pitch_name(pitch_name):
   '''True when `pitch_name` string has the form of a
   LilyPond pitch name in English. ::

      abjad> pitchtools.is_pitch_name('c')
      True
      abjad> pitchtools.is_pitch_name('cs')
      True
      abjad> pitchtools.is_pitch_name('css')
      True
      abjad> pitchtools.is_pitch_name('cqs')
      True
      abjad> pitchtools.is_pitch_name('ctqs')
      True

   Otherwise false. ::

      abjad> pitchtools.is_pitch_name('foo')
      False

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.is_name( )`` to
      ``pitchtools.is_pitch_name( )``.
   '''

   if not isinstance(pitch_name, str):
      raise TypeError('must be str.')

   return pitch_name in _pitch_names


_diatonic_names = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
_accidental_names = ['', '!', 's', 'f', 'ss', 'ff', 'qs', 'qf', 'tqs', 'tqf']
_pitch_names = [ ]

for _dn in _diatonic_names:
   for _an in _accidental_names:
      _pitch_names.append(_dn + _an)
