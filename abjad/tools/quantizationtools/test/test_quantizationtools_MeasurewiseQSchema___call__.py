# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import quantizationtools
import pytest


def test_quantizationtools_MeasurewiseQSchema___call___01():

    schema = quantizationtools.MeasurewiseQSchema()

    target = schema(5000)
