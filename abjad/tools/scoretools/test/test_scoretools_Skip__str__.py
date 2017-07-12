# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Skip__str___01():

    skip = abjad.Skip((1, 4))

    assert str(skip) == 's4'
