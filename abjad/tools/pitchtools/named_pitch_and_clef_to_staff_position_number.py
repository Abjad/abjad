# -*- encoding: utf-8 -*-


def named_pitch_and_clef_to_staff_position_number(pitch, clef):
    r'''Change named `pitch` and `clef` to staff position number:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> clef = marktools.ClefMark('treble')
        >>> for note in staff:
        ...   written_pitch = note.written_pitch
        ...   number = pitchtools.named_pitch_and_clef_to_staff_position_number(
        ...         written_pitch, clef)
        ...   print '%s\t%s' % (written_pitch, number)
        c'    -6
        d'    -5
        e'    -4
        f'    -3
        g'    -2
        a'    -1
        b'    0
        c''   1

    Returns integer.
    '''
    return abs(pitch.diatonic_pitch_number) + clef.middle_c_position
