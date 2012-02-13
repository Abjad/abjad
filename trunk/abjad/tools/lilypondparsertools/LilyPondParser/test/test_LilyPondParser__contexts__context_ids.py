from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__contexts__context_ids_01():
    target = Staff(notetools.make_notes([0, 2, 4, 5, 7], (1, 8)))
    target.name = 'foo'

    r'''\context Staff = "foo" {
        c'8
        d'8
        e'8
        f'8
        g'8
    }
    '''

    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result
