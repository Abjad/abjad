from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__containers__Container_01( ):
    parser = LilyPondParser()
    target = Container()
    result = parser(target.format)
    assert target.format == result.format and target is not result
