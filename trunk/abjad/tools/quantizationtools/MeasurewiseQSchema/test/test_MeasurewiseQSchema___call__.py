from abjad.tools import contexttools
from abjad.tools import quantizationtools
import py


def test_MeasurewiseQSchema___call___01():

    schema = quantizationtools.MeasurewiseQSchema()

    target = schema(5000)
