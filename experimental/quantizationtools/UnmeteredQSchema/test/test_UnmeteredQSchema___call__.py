from abjad.tools import contexttools
from experimental import quantizationtools


def test_UnmeteredQSchema___call___01():

    schema = quantizationtools.UnmeteredQSchema()

    target = schema(5000)

