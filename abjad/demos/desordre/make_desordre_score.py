# -*- coding: utf-8 -*-
import abjad


def make_desordre_score(pitches):
    '''Makes Désordre score.
    '''

    assert len(pitches) == 2
    staff_group = abjad.StaffGroup()
    staff_group.context_name = 'PianoStaff'

    # build the music
    for hand in pitches:
        staff = abjad.demos.desordre.make_desordre_staff(hand)
        staff_group.append(staff)

    # set clef and key signature to left hand staff
    clef = abjad.Clef('bass')
    abjad.attach(clef, staff_group[1])
    key_signature = abjad.KeySignature('b', 'major')
    abjad.attach(key_signature, staff_group[1])

    # wrap the piano staff in a score
    score = abjad.Score([staff_group])

    return score
