from abjad.tools import contexttools
from experimental import quantizationtools


def test_MeteredQSchema___call___01():

    schema = quantizationtools.MeteredQSchema()

    target = schema(5000)
