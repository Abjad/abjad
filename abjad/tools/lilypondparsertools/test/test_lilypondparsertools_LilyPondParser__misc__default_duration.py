import abjad
import pytest


def test_lilypondparsertools_LilyPondParser__misc__default_duration_01():

    maker = abjad.NoteMaker()
    target = abjad.Container(maker(
        [0],
        [(1, 4), (1, 2), (1, 2), (1, 8), (1, 8), (3, 16), (3, 16)]
        ))
    abjad.attach(abjad.Multiplier(5, 17), target[-2])
    abjad.attach(abjad.Multiplier(5, 17), target[-1])

    assert format(target) == abjad.String.normalize(
        r'''
        {
            c'4
            c'2
            c'2
            c'8
            c'8
            c'8. * 5/17
            c'8. * 5/17
        }
        '''
        )

    string = r'''{ c' c'2 c' c'8 c' c'8. * 5/17 c' }'''

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result
