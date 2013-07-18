from abjad import *
from abjad.tools import tonalanalysistools


def test_SuspensionIndicator__init_empty_01():

    t = tonalanalysistools.SuspensionIndicator()

    assert t.start is None
    assert t.stop is None
