from abjad.tools import contexttools
from experimental import quantizationtools
import py
py.test.skip('FIXME')


def test_BeatwiseQSchema___call___01():

    schema = quantizationtools.BeatwiseQSchema()

    target = schema(5000)

