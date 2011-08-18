from abjad import *
from abjad.tools import tonalitytools


def test_SuspensionIndicator_title_string_01():

    t = tonalitytools.SuspensionIndicator(4, 3)
    assert t.title_string == 'FourThreeSuspension'

    t = tonalitytools.SuspensionIndicator(('flat', 2), 1)
    assert t.title_string == 'FlatTwoOneSuspension'

    t = tonalitytools.SuspensionIndicator()
    assert t.title_string == ''
