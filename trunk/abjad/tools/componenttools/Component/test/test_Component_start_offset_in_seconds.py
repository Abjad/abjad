from abjad import *
import py.test
#import py
#py.test.skip('update me to use start_offset_in_seconds property.')


def test_Component_start_offset_in_seconds_01():
    '''Offset seconds can not calculate without excplit tempo indication.
    '''

    t = Staff("c'8 d'8 e'8 f'8")

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert py.test.raises(MissingTempoError, 't[0].start_offset_in_seconds')
    assert py.test.raises(MissingTempoError, 't[0].start_offset_in_seconds')


def test_Component_start_offset_in_seconds_02():
    '''Offset seconds work with explicit tempo indication.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    contexttools.TempoMark(Duration(1, 8), 48, target_context=Staff)(t)

    r'''
    \new Staff {
        \tempo 8=48
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t[0].start_offset_in_seconds == Duration(0)
    assert t[1].start_offset_in_seconds == Duration(5, 4)
