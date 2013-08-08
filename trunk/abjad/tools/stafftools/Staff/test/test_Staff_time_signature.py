# -*- encoding: utf-8 -*-
from abjad import *


def test_Staff_time_signature_01():
    r'''Force time signature on nonempty staff.
    '''

    staff = Staff(Note("c'4") * 8)
    contexttools.TimeSignatureMark((2, 4))(staff)

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

    assert testtools.compare(
        staff.lilypond_format,
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


def test_Staff_time_signature_02():
    r'''Force time signature on empty staff.
    '''

    staff = Staff([])
    contexttools.TimeSignatureMark((2, 4))(staff)

    r'''
    \new Staff {
        \time 2/4
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            \time 2/4
        }
        '''
        )


def test_Staff_time_signature_03():
    r'''Staff time signature carries over to staff-contained leaves.
    '''

    staff = Staff(Note("c'4") * 8)
    contexttools.TimeSignatureMark((2, 4))(staff)
    for x in staff:
        assert more(x).get_effective_context_mark(contexttools.TimeSignatureMark) \
            == contexttools.TimeSignatureMark((2, 4))


def test_Staff_time_signature_04():
    r'''Staff time signature set and then clear.
    '''

    staff = Staff(Note("c'4") * 8)
    contexttools.TimeSignatureMark((2, 4))(staff)
    more(staff).get_effective_context_mark(contexttools.TimeSignatureMark).detach()
    for leaf in staff:
        assert more(leaf).get_effective_context_mark(
            contexttools.TimeSignatureMark) is None
