def named_chromatic_pitch_and_clef_to_staff_position_number(pitch, clef):
   r'''.. versionadded:: 1.1.2

   Change named chromatic `pitch` and `clef` to staff position number::

      abjad> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
      abjad> clef = contexttools.ClefMark('treble')
      abjad> for note in staff:
      ...   pitch = note.pitch
      ...   number = pitchtools.named_chromatic_pitch_and_clef_to_staff_position_number(pitch, clef)
      ...   print '%s\t%s' % (pitch, number)
      c'    -6
      d'    -5
      e'    -4
      f'    -3
      g'    -2
      a'    -1
      b'    0
      c''   1

   Return integer.
   '''

   return abs(pitch.numbered_diatonic_pitch) + clef.middle_c_position   
