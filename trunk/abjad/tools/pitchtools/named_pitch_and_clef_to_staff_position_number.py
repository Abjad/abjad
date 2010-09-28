def named_pitch_and_clef_to_staff_position_number(pitch, clef):
   r'''.. versionadded:: 1.1.2

   Convert `pitch` and `clef` to staff position number. ::

      abjad> staff = Staff(macros.scale(8))
      abjad> clef = contexttools.ClefMark('treble')
      abjad> for note in staff:
      ...   pitch = note.pitch
      ...   number = pitchtools.named_pitch_and_clef_to_staff_position_number(pitch, clef)
      ...   print '%s\t%s' % (pitch, number)
      c'    -6
      d'    -5
      e'    -4
      f'    -3
      g'    -2
      a'    -1
      b'    0
      c''   1

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.pitch_and_clef_to_staff_position_number( )`` to
      ``pitchtools.named_pitch_and_clef_to_staff_position_number( )``.
   '''

   return pitch.altitude + clef.middle_c_position   
