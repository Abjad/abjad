from abjad import *
from abjad.tools import tonalanalysistools


def test_SuspensionIndicator_is_empty_01():

    t = tonalanalysistools.SuspensionIndicator()

    assert t.is_empty
