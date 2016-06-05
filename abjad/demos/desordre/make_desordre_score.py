# -*- coding: utf-8 -*-
import abjad
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach


def make_desordre_score(pitches):
    '''Makes Désordre score.
    '''

    assert len(pitches) == 2
    staff_group = scoretools.StaffGroup()
    staff_group.context_name = 'PianoStaff'

    # build the music
    for hand in pitches:
        staff = abjad.demos.desordre.make_desordre_staff(hand)
        staff_group.append(staff)

    # set clef and key signature to left hand staff
    clef = indicatortools.Clef('bass')
    attach(clef, staff_group[1])
    key_signature = indicatortools.KeySignature('b', 'major')
    attach(key_signature, staff_group[1])

    # wrap the piano staff in a score
    score = scoretools.Score([staff_group])

    return score