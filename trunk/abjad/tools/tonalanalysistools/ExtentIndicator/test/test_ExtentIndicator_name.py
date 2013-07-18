from abjad import *
from abjad.tools import tonalanalysistools


def test_ExtentIndicator_name_01():

    assert tonalanalysistools.ExtentIndicator(5).name == 'triad'
    assert tonalanalysistools.ExtentIndicator(7).name == 'seventh'
    assert tonalanalysistools.ExtentIndicator(9).name == 'ninth'
