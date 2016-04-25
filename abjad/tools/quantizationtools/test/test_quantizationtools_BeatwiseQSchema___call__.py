# -*- coding: utf-8 -*-
from abjad import *


def test_quantizationtools_BeatwiseQSchema___call___01():

    schema = quantizationtools.BeatwiseQSchema()

    target = schema(5000)
