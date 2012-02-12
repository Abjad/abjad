import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


py.test.skip('Not yet written.')
def test_LilyPondParser__marks__KeySignatureMark_01():
    target = None
    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result

