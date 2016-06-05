# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Staff_time_signature_01():
    r'''Force time signature on nonempty staff.
    '''

    staff = Staff(Note("c'4") * 8)
    time_signature = TimeSignature((2, 4))
    attach(time_signature, staff)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \time 2/4
            c'4
            c'4
            c'4
            c'4
            c'4
            c'4
            c'4
            c'4
        }
        '''
        )


def test_scoretools_Staff_time_signature_02():
    r'''Force time signature on empty staff.
    '''

    staff = Staff([])
    time_signature = TimeSignature((2, 4))
    attach(time_signature, staff)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \time 2/4
        }
        '''
        )


def test_scoretools_Staff_time_signature_03():
    r'''Staff time signature carries over to staff-contained leaves.
    '''

    staff = Staff(Note("c'4") * 8)
    time_signature = TimeSignature((2, 4))
    attach(time_signature, staff)
    for x in staff:
        assert inspect_(x).get_effective(TimeSignature) \
            == TimeSignature((2, 4))


def test_scoretools_Staff_time_signature_04():
    r'''Staff time signature set and then clear.
    '''

    staff = Staff(Note("c'4") * 8)
    time_signature = TimeSignature((2, 4))
    attach(time_signature, staff)
    detach(time_signature, staff)
    for leaf in staff:
        assert inspect_(leaf).get_effective(
            TimeSignature) is None
