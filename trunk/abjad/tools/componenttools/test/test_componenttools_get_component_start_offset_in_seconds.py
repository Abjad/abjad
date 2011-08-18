from abjad import *
import py.test


def test_componenttools_get_component_start_offset_in_seconds_01():
    '''Offset seconds can not calculate without excplit tempo indication.'''

    t = Staff("c'8 d'8 e'8 f'8")

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert py.test.raises(MissingTempoError,
        'componenttools.get_component_start_offset_in_seconds(t[0])')
    assert py.test.raises(MissingTempoError,
        'componenttools.get_component_stop_offset_in_seconds(t[0])')


def test_componenttools_get_component_start_offset_in_seconds_02():
    '''Offset seconds work with explicit tempo indication.'''

    t = Staff("c'8 d'8 e'8 f'8")
    contexttools.TempoMark(Duration(1, 8), 48, target_context = Staff)(t)

    r'''
    \new Staff {
        \tempo 8=48
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert componenttools.get_component_start_offset_in_seconds(t[0]) == Duration(0)
    assert componenttools.get_component_start_offset_in_seconds(t[1]) == Duration(5, 4)
