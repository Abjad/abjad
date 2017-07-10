# -*- coding: utf-8 -*-
import abjad
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__contexts__context_ids_01():

    maker = abjad.NoteMaker()
    notes = maker([0, 2, 4, 5, 7], (1, 8))
    target = Staff(notes)
    target.name = 'foo'

    assert format(target) == String.normalize(
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
