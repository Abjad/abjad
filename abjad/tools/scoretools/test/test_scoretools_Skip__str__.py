# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Skip__str___01():

    skip = scoretools.Skip((1, 4))

    assert str(skip) == 's4'
