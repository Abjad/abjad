# -*- coding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__indicators__BarLine_01():

    target = Staff(scoretools.make_notes(["e'", "d'", "c'"], [(1, 4), (1, 4), (1, 2)]))
    bar_line = indicatortools.BarLine('|.')
    attach(bar_line, target[-1])

    assert format(target) == stringtools.normalize(
        r'''
        \new Staff {
            e'4
            d'4
            c'2
            \bar "|."
        }
        '''
        )

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    items = inspect_(result[2]).get_indicators()
    assert 1 == len(items) and isinstance(items[0], indicatortools.BarLine)
