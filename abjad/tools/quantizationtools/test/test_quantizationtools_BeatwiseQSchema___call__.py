# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import quantizationtools
import pytest


def test_quantizationtools_BeatwiseQSchema___call___01():

    schema = quantizationtools.BeatwiseQSchema()

    target = schema(5000)
