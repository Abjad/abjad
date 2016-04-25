# -*- coding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__lilypondfile__ScoreBlock_01():

    target = lilypondfiletools.Block(name='score')
    target.items.append(Score())
    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
