from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__functions__grace_01():
    target = Container([
        Note("c'4"),
        Note("d'4"),
        Note("e'2")
    ])
    grace = gracetools.GraceContainer([
        Note("g''16"),
        Note("fs''16")
    ])
    grace(target[2])

    r'''{
        c'4
        d'4
        \grace {
            g''16
            fs''16
        }
        e'2
    }
    '''

    input = r"{ c'4 d'4 \grace { g''16 fs''16} e'2 }"
    parser = LilyPondParser()
    result = parser(input)
    assert target.lilypond_format == result.lilypond_format and target is not result

