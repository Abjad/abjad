# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__containers__nesting_01():

    target = Container([
        Container([]),
        Container([
            Container([])
        ])
    ])

    assert systemtools.TestManager.compare(
        target,
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

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
