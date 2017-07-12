# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Staff_time_signature_01():
    r'''Force time signature on nonempty staff.
    '''

    staff = abjad.Staff(abjad.Note("c'4") * 8)
    time_signature = abjad.TimeSignature((2, 4))
    abjad.attach(time_signature, staff)

    assert format(staff) == abjad.String.normalize(
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

    staff = abjad.Staff([])
    time_signature = abjad.TimeSignature((2, 4))
    abjad.attach(time_signature, staff)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \time 2/4
        }
        '''
        )


def test_scoretools_Staff_time_signature_03():
    r'''Staff time signature carries over to staff-contained leaves.
    '''

    staff = abjad.Staff(abjad.Note("c'4") * 8)
    time_signature = abjad.TimeSignature((2, 4))
    abjad.attach(time_signature, staff)
    for x in staff:
        assert abjad.inspect(x).get_effective(abjad.TimeSignature) \
            == abjad.TimeSignature((2, 4))


def test_scoretools_Staff_time_signature_04():
    r'''Staff time signature set and then clear.
    '''

    staff = abjad.Staff(abjad.Note("c'4") * 8)
    time_signature = abjad.TimeSignature((2, 4))
    abjad.attach(time_signature, staff)
    abjad.detach(time_signature, staff)
    for leaf in staff:
        assert abjad.inspect(leaf).get_effective(
            abjad.TimeSignature) is None
