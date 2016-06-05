# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_make_repeated_notes_from_time_signature_01():
    r'''Make repeated notes from integer pair.
    '''

    notes = scoretools.make_repeated_notes_from_time_signature((5, 32), pitch="d''")
    staff = Staff(notes)

    assert inspect_(staff).is_well_formed()
    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            d''32
            d''32
            d''32
            d''32
            d''32
        }
        '''
        )


def test_scoretools_make_repeated_notes_from_time_signature_02():
    r'''Make repeated notes from time signature.
    '''

    time_signature = TimeSignature((5, 32))
    notes = scoretools.make_repeated_notes_from_time_signature(time_signature, pitch="d''")
    staff = Staff(notes)

    assert inspect_(staff).is_well_formed()
    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            d''32
            d''32
            d''32
            d''32
            d''32
        }
        '''
        )
