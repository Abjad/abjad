# -*- coding: utf-8 -*-
import abjad


def test_lilypondparsertools_LilyPondParser__containers__Container_01():
    parser = abjad.lilypondparsertools.LilyPondParser()
    target = abjad.Container()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
