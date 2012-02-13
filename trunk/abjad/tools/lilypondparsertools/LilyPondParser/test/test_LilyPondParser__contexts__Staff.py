from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__contexts__Staff_01():
    target = Staff([])

    r'''\new Staff {
    }
    '''

    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result


def test_LilyPondParser__contexts__Staff_02():
    target = Staff([])
    target.is_parallel = True
    target.append(Voice(notetools.make_notes([0, 2, 4, 5, 7, 9, 11, 12], (1, 8))))
    target.append(Voice(notetools.make_notes([0, 2, 4, 5, 7, 9, 11, 12], (1, 8))))

    r'''\new Staff <<
        \new Voice {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
            b'8
            c''8
        }
        \new Voice {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
            b'8
            c''8
        }
    >>
    '''

    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result
