import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__lilypondfile__ScoreBlock_01():
    target = lilypondfiletools.ScoreBlock()
    target.append(Score())
    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and target is not result
