import abjad
from abjad.tools import quantizationtools


def test_quantizationtools_MeasurewiseQSchema___call___01():

    schema = quantizationtools.MeasurewiseQSchema()

    target = schema(5000)
