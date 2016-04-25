# -*- coding: utf-8 -*-
from abjad import *


def test_quantizationtools_MeasurewiseQSchema___call___01():

    schema = quantizationtools.MeasurewiseQSchema()

    target = schema(5000)
