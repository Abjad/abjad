# -*- encoding: utf-8 -*-
from abjad import *


def test_TimeSignatureMark_numerator_01():
    r'''Time signature numerator is read / write.
    '''

    time_signature = contexttools.TimeSignatureMark((3, 8))
    assert time_signature.numerator == 3

    time_signature.numerator = 4
    assert time_signature.numerator == 4



def test_TimeSignatureMark_numerator_02():
    r'''Time signature formats correctly after numerator change.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    time_signature = contexttools.TimeSignatureMark((4, 8))(staff)
    time_signature.numerator = 2

    r'''
    \new Staff {
        \time 2/8
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \time 2/8
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )
