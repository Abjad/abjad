from abjad.tools import contexttools
from abjad.tools import quantizationtools
import py


def test_BeatwiseQSchema___call___01():

    schema = quantizationtools.BeatwiseQSchema()

    target = schema(5000)
