from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__misc__version_string_01():
    '''Version strings are ignored.'''
    target = Staff()
    input = r'''\version "2.14.2" \new Staff { }'''
    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result

