from abjad import *
from abjad.tools import tonalanalysistools


def test_SuspensionIndicator_figured_bass_string_01():

    t = tonalanalysistools.SuspensionIndicator(4, 3)
    assert t.figured_bass_string == '4-3'

    t = tonalanalysistools.SuspensionIndicator(('flat', 2), 1)
    assert t.figured_bass_string == 'b2-1'

    t = tonalanalysistools.SuspensionIndicator()
    assert t.figured_bass_string == ''
