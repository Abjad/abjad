# -*- encoding: utf-8 -*-

from abjad import *
from abjad.demos.desordre.make_desordre_staff import make_desordre_staff


def make_desordre_score(pitches):
    '''Returns a complete PianoStaff with Ligeti music!'''

    assert len(pitches) == 2
    piano_staff = scoretools.PianoStaff()

    # build the music...
    for hand in pitches:
        staff = make_desordre_staff(hand)
        piano_staff.append(staff)

    # set clef and key signature to left hand staff...
    contexttools.ClefMark('bass')(piano_staff[1])
    contexttools.KeySignatureMark('b', 'major')(piano_staff[1])

    # wrap the piano staff in a score, and return
    score = Score([piano_staff])

    return score
