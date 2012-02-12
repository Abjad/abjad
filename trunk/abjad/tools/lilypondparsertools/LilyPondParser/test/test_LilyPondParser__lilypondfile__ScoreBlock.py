import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


py.test.skip('LilyPondParser refuses to parse empty ScoreBlock.')
def test_LilyPondParser__lilypondfile__ScoreBlock_01():
    target = lilypondfiletools.ScoreBlock()
    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result

