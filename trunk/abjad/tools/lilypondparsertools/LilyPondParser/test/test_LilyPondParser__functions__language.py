from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__functions__language_01():
    target = Container([
        Note("cs'8"),
        Note("ds'8"),
        Note("ff'8")
    ])

    r'''{
        cs'8
        ds'8
        ff'8
    }
    '''

    input = r"\language nederlands { cis'8 dis'8 fes'8 }"
    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result

