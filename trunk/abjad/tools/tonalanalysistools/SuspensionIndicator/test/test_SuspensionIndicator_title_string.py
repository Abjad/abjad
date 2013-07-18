from abjad import *
from abjad.tools import tonalanalysistools


def test_SuspensionIndicator_title_string_01():

    t = tonalanalysistools.SuspensionIndicator(4, 3)
    assert t.title_string == 'FourThreeSuspension'

    t = tonalanalysistools.SuspensionIndicator(('flat', 2), 1)
    assert t.title_string == 'FlatTwoOneSuspension'

    t = tonalanalysistools.SuspensionIndicator()
    assert t.title_string == ''
