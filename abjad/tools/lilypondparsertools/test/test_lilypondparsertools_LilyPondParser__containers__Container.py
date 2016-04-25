# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__containers__Container_01():
    parser = LilyPondParser()
    target = Container()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
