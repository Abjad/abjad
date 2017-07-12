# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Rest___str___01():

    rest = abjad.Rest((1, 4))

    assert str(rest) == 'r4'
