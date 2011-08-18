from abjad import *


def test_SchemeString___init___01():

    t = Note(0, (1, 16))
    t.override.stem.stroke_style = schemetools.SchemeString('grace')

    r'''
    \once \override Stem #'stroke-style = #"grace"
    c'16
    '''

    assert t.format == '\\once \\override Stem #\'stroke-style = #"grace"\nc\'16'
