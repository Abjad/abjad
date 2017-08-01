# -*- coding: utf-8 -*-
import abjad


def test_lilypondparsertools_LilyPondParser__containers__nesting_01():

    target = abjad.Container([
        abjad.Container([]),
        abjad.Container([
            abjad.Container([])
        ])
    ])

    assert format(target) == abjad.String.normalize(
        r'''
        {
            {
            }
            {
                {
                }
            }
        }
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
