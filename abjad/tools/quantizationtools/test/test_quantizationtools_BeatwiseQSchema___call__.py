# -*- coding: utf-8 -*-
import abjad
from abjad.tools import quantizationtools


def test_quantizationtools_BeatwiseQSchema___call___01():

    schema = quantizationtools.BeatwiseQSchema()

    target = schema(5000)
