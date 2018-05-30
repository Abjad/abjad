import abjad


def test_LilyPondParser__contexts__with_blocks_01():

    target = abjad.Staff([])

    r'''
    \new Staff {
    }
    '''

    string = r'''\new Staff \with { } {
    }
    '''

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result
