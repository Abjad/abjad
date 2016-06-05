# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_make_repeated_notes_from_time_signatures_01():
    r'''Make repeated notes from list of integer pairs.
    '''

    notes = scoretools.make_repeated_notes_from_time_signatures([(2, 8), (3, 32)], pitch = "d''")
    assert len(notes) == 2

    notes = sequencetools.flatten_sequence(notes)
    staff = Staff(notes)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            d''8
            d''8
            d''32
            d''32
            d''32
        }
        '''
        )
    assert inspect_(staff).is_well_formed()
