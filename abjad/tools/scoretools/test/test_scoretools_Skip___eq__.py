# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Skip___eq___01():

    skip_1 = abjad.Skip((1, 4))
    skip_2 = abjad.Skip((1, 4))
    skip_3 = abjad.Skip((1, 8))

    assert not skip_1 == skip_2
    assert not skip_1 == skip_3
    assert not skip_2 == skip_3
