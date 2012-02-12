from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__contexts__StaffGroup_01():
    target = scoretools.StaffGroup([])

    r'''\new StaffGroup <<
    >>
    '''

    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result

