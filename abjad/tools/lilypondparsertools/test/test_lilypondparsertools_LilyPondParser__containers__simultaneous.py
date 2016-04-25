# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__containers__simultaneous_01():

    target = Container()
    target.is_simultaneous = True
    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
