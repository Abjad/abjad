from abjad import *


def test_SchemeBoolean___init___01():

    t = Note(0, (1, 16))
    t.override.stem.transparent = schemetools.SchemeBoolean(True)

    r'''
    \once \override Stem #'transparent = ##t
    c'16
    '''

    assert t.format == '\\once \\override Stem #\'transparent = ##t\nc\'16'
