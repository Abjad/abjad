# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_containertools_Container_get_duration_01():
    r'''Container duration in seconds equals
    sum of leaf durations in seconds.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    tempo = contexttools.TempoMark(Duration(1, 4), 38)
    attach(tempo, staff)
    tempo = contexttools.TempoMark(Duration(1, 4), 42)
    attach(tempo, staff[2])
    score = Score([staff])

    assert testtools.compare(
        score,
        r'''
        \new Score <<
            \new Staff {
                \tempo 4=38
                c'8
                d'8
                \tempo 4=42
                e'8
                f'8
            }
        >>
        '''
        )

    assert inspect(score).get_duration(in_seconds=True) == Duration(400, 133)


def test_containertools_Container_get_duration_02():
    r'''Container can not calculate duration in seconds
    without tempo indication.
    '''

    container = Container("c'8 d'8 e'8 f'8")
    assert py.test.raises(MissingTempoError, 
        'inspect(container).get_duration(in_seconds=True)')
