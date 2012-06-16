from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__containers__nesting_01():
    target = Container([
        Container([]), 
        Container([
            Container([])
        ])
    ])

    r'''{
        {
        }
        {
            {
            }
        }
    }
    '''

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and target is not result
