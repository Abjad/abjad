from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__marks__ClefMark_01():
    target = Staff([Note(0, 1)])
    contexttools.ClefMark('bass')(target[0])

    r'''\new Staff {
        \clef "bass"
        c'1
    }
    '''

    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result
    assert 1 == len(contexttools.get_clef_marks_attached_to_component(result[0]))
