import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__marks__BarLine_01():
    target = Staff(notetools.make_notes(["e'", "d'", "c'"], [(1, 4), (1, 4), (1, 2)]))
    marktools.BarLine('|.')(target[-1])

    r'''\new Staff {
        e'4
        d'4
        c'2
        \bar "|."
    }
    '''

    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result
    marks = marktools.get_marks_attached_to_component(result[2])
    assert 1 == len(marks) and isinstance(marks[0], marktools.BarLine)
