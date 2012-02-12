from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__leaves__Skip_01():
    target = skiptools.Skip((3, 8))
    parser = LilyPondParser()
    result = parser('{ %s }' % target.format)
    assert target.format == result[0].format and target is not result[0]

