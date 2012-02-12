from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__containers__parallel_01():
    target = Container()
    target.is_parallel = True
    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result
