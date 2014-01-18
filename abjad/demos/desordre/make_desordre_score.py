# -*- encoding: utf-8 -*-
from abjad import *
from abjad.demos.desordre.make_desordre_staff import make_desordre_staff


def make_desordre_score(pitches):
    '''Returns a complete piano staff with Ligeti music.
    '''

    assert len(pitches) == 2
    staff_group = StaffGroup()
    staff_group.context_name = 'PianoStaff'

    # build the music
    for hand in pitches:
        staff = make_desordre_staff(hand)
        staff_group.append(staff)

    # set clef and key signature to left hand staff
    clef = indicatortools.Clef('bass')
    attach(clef, staff_group[1])
    key_signature = KeySignature('b', 'major')
    attach(key_signature, staff_group[1])

    # wrap the piano staff in a score
    score = scoretools.Score([staff_group])

    return score
