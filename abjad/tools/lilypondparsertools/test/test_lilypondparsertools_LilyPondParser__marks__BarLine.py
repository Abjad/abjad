# -*- encoding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__marks__BarLine_01():

    target = Staff(scoretools.make_notes(["e'", "d'", "c'"], [(1, 4), (1, 4), (1, 2)]))
    bar_line = marktools.BarLine('|.')
    attach(bar_line, target[-1])

    assert systemtools.TestManager.compare(
        target,
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
    items = inspect(result[2]).get_attached_items()
    assert 1 == len(items) and isinstance(items[0], marktools.BarLine)
