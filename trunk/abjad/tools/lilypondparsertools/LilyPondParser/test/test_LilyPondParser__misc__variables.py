from abjad import *
from abjad.tools.lilypondparsertools import *


def test_LilyPondParser__misc__variables_01():
    target = Staff([
        Container([
            Container([
                Container([
                    Container([Note(0, (1, 8))]),
                    Note(2, (1, 8)),
                    Note(4, (1, 4))
                ]),
                Note(5, (1, 4)),
                Note(7, (1, 2))
            ]),
            Note(9, (1, 2)),
            Note(11, 1)
        ]),
        Note(12, 1)
    ])

    r'''\new Staff {
        {
            {
                {
                    {
                        c'8
                    }
                    d'8
                    e'4
                }
                f'4
                g'2
            }
            a'2
            b'1
        }
        c''1
    }
    '''

    input = r'''
        foo = { c'8 }
        foo = { \foo d' e'4 }
        foo = { \foo f' g'2 }
        foo = { \foo a' b'1 }
        \new Staff { \foo c'' }
    '''

    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result
