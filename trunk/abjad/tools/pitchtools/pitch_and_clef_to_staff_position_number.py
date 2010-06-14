def pitch_and_clef_to_staff_position_number(pitch, clef):
   r'''.. versionadded:: 1.1.2

   Convert `pitch` and `clef` to staff position number. ::

      abjad> staff = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(8))
      abjad> clef = Clef('treble')
      abjad> for note in staff:
      ...   pitch = note.pitch
      ...   number = pitchtools.pitch_and_clef_to_staff_position_number(pitch, clef)
      ...   print '%s\t%s' % (pitch, number)
      c'    -6
      d'    -5
      e'    -4
      f'    -3
      g'    -2
      a'    -1
      b'    0
      c''   1
   '''

   return pitch.altitude + clef.middle_c_position   
