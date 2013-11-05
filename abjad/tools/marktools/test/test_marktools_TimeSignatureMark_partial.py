# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_TimeSignatureMark_partial_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    time_signature = marktools.TimeSignatureMark((2, 8), partial=Duration(1, 8))
    attach(time_signature, staff)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \partial 8
            \time 2/8
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_marktools_TimeSignatureMark_partial_02():
    r'''Time signature partial is read / write.
    '''

    time_signature = marktools.TimeSignatureMark((3, 8), partial = Duration(1, 8))
    assert time_signature.partial == Duration(1, 8)

    time_signature.partial = Duration(2, 8)
    assert time_signature.partial == Duration(2, 8)


def test_marktools_TimeSignatureMark_partial_03():
    r'''Time signature partial can be cleared with none.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8")
    time_signature = time_signature = marktools.TimeSignatureMark((4, 8))
    attach(time_signature, staff)
    time_signature.partial = Duration(2, 8)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \partial 4
            \time 4/8
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
        }
        '''
        )

    time_signature.partial = None

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
        }
        '''
        )
