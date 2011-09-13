from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch


def clef_and_staff_position_number_to_named_chromatic_pitch(clef, staff_position_number):
    r'''.. versionadded:: 2.0

    Change `clef` and `staff_position_number` to named chromatic pitch::

        abjad> clef = contexttools.ClefMark('treble')
        abjad> for n in range(-6, 6):
        ...   pitch = pitchtools.clef_and_staff_position_number_to_named_chromatic_pitch(clef, n)
        ...   print '%s\t%s\t%s' % (clef.clef_name, n, pitch)
        treble   -6 c'
        treble   -5 d'
        treble   -4 e'
        treble   -3 f'
        treble   -2 g'
        treble   -1 a'
        treble   0  b'
        treble   1  c''
        treble   2  d''
        treble   3  e''
        treble   4  f''
        treble   5  g''

    Return named chromatic pitch.
    '''

    position_residue_to_pitch_name = {
        0: 'b', 1: 'c', 2: 'd', 3: 'e', 4: 'f', 5: 'g', 6: 'a'}

    n = staff_position_number - (6 + clef.middle_c_position)
    #position_residue = staff_position_number % 7
    position_residue = n % 7
    pitch_name = position_residue_to_pitch_name[position_residue]
    #octave = 4 + int(staff_position_number / 7) + 1
    octave = 4 + int(n / 7) + 1
    if pitch_name == 'b':
        octave -= 1
    pitch = NamedChromaticPitch(pitch_name, octave)

    return pitch
