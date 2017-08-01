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
        staff = abjad.demos.ligeti.make_desordre_staff(hand)
        staff_group.append(staff)

    # set clef and key signature to left hand staff
    leaf = abjad.inspect(staff_group[1]).get_leaf(0)
    clef = abjad.Clef('bass')
    abjad.attach(clef, leaf)
    key_signature = abjad.KeySignature('b', 'major')
    abjad.attach(key_signature, leaf)

    # wrap the piano staff in a score
    score = abjad.Score([staff_group])

    return score
