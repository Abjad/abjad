from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser
import py.test


def test_LilyPondParser__marks__TempoMark_01():
    target = Score([Staff([Note(0, 1)])])
    contexttools.TempoMark("As fast as possible", target_context=Staff)(target.leaves[0])

    r'''\new Score <<
        \new Staff {
            \tempo "As fast as possible"
            c'1
        }
    >>
    '''

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and target is not result
    assert 1 == len(contexttools.get_tempo_marks_attached_to_component(result.leaves[0]))


def test_LilyPondParser__marks__TempoMark_02():
    target = Score([Staff([Note(0, 1)])])
    contexttools.TempoMark((1, 4), 60, target_context=Staff)(target.leaves[0])

    r'''\new Score <<
        \new Staff {
            \tempo 4=60
            c'1
        }
    >>
    '''

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and target is not result
    assert 1 == len(contexttools.get_tempo_marks_attached_to_component(result.leaves[0]))


def test_LilyPondParser__marks__TempoMark_03():
    target = Score([Staff([Note(0, 1)])])
    contexttools.TempoMark((1, 4), (59, 63), target_context=Staff)(target.leaves[0])

    r'''\new Score <<
        \new Staff {
            \tempo 4=59~63
            c'1
        }
    >>
    '''

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and target is not result
    assert 1 == len(contexttools.get_tempo_marks_attached_to_component(result.leaves[0]))


def test_LilyPondParser__marks__TempoMark_04():
    target = Score([Staff([Note(0, 1)])])
    contexttools.TempoMark("Like a majestic swan, alive with youth and vigour!", \
        (1, 4), 60, target_context=Staff)(target.leaves[0])

    r'''\new Score <<
        \new Staff {
            \tempo "Like a majestic swan, alive with youth and vigour!" 4=60
            c'1
        }
    >>
    '''

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and target is not result
    assert 1 == len(contexttools.get_tempo_marks_attached_to_component(result.leaves[0]))


def test_LilyPondParser__marks__TempoMark_05():
    target = Score([Staff([Note(0, 1)])])
    contexttools.TempoMark("Faster than a thousand suns",
        (1, 16), (34, 55), target_context=Staff)(target.leaves[0])

    r'''\new Score <<
        \new Staff {
            \tempo "Faster than a thousand suns" 16=34~55
            c'1
        }
    >>
    '''

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and target is not result
    assert 1 == len(contexttools.get_tempo_marks_attached_to_component(result.leaves[0]))
