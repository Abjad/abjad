from abjad import *
import py.test


def test_Container_duration_in_seconds_01():
    '''Container duration in seconds equals
    sum of leaf durations in seconds.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    contexttools.TempoMark(Duration(1, 4), 38)(t)
    contexttools.TempoMark(Duration(1, 4), 42)(t[2])
    score = Score([t])

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

    assert score.duration_in_seconds == Duration(400, 133)


def test_Container_duration_in_seconds_02():
    '''Container can not calculate duration in seconds
        without tempo indication.'''

    t = Container("c'8 d'8 e'8 f'8")
    assert py.test.raises(MissingTempoError, 't.duration_in_seconds')
