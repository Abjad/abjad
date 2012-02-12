from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__leaves__Rest_01():
    target = Rest((1, 8))
    parser = LilyPondParser()
    result = parser('{ %s }' % target.format)
    assert target.format == result[0].format and target is not result[0]

