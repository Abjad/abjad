from abjad import *


def test_PitchRangeInventory__repr_with_tools_package_01():

    inventory = pitchtools.PitchRangeInventory(['[A0, C8]', '[C4, D5]'])

    assert inventory._fully_qualified_repr == "pitchtools.PitchRangeInventory([pitchtools.PitchRange('[A0, C8]'), pitchtools.PitchRange('[C4, D5]')])"
