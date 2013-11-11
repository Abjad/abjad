# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_TimeSignature_numerator_01():
    r'''Time signature numerator is read / write.
    '''

    time_signature = TimeSignature((3, 8))
    assert time_signature.numerator == 3

    time_signature.numerator = 4
    assert time_signature.numerator == 4



def test_marktools_TimeSignature_numerator_02():
    r'''Time signature formats correctly after numerator change.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    time_signature = TimeSignature((4, 8))
    attach(time_signature, staff)
    time_signature.numerator = 2

    assert systemtools.TestManager.compare(
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
