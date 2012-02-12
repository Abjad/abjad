from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__lilypondfile__LilyPondFile_01():
    input = '{ c } { c } { c } { c }'
    parser = LilyPondParser()
    result = parser(input)
    assert isinstance(result, lilypondfiletools.LilyPondFile)

