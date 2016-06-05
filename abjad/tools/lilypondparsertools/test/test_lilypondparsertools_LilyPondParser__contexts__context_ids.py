# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__contexts__context_ids_01():

    target = Staff(scoretools.make_notes([0, 2, 4, 5, 7], (1, 8)))
    target.name = 'foo'

    assert format(target) == stringtools.normalize(
        r'''
        \context Staff = "foo" {
            c'8
            d'8
            e'8
            f'8
            g'8
        }
        '''
        )

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
