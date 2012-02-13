from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__contexts__with_blocks_01():
    target = Staff([])

    r'''\new Staff {
    }
    '''

    input = r'''\new Staff \with { } {
    }
    '''

    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result
