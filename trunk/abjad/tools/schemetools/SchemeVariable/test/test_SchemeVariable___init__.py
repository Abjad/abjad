from abjad import *


def test_SchemeVariable___init___01():

    t = Note("c'4")
    t.override.stem.direction = schemetools.SchemeVariable('DOWN')

    r'''
    \once \override Stem #'direction = #DOWN
    c'4
    '''

    assert t.format == "\\once \\override Stem #'direction = #DOWN\nc'4"
