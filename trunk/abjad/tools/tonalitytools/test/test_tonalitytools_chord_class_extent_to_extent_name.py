from abjad import *
from abjad.tools import tonalitytools
import py.test


def test_tonalitytools_chord_class_extent_to_extent_name_01():

    assert tonalitytools.chord_class_extent_to_extent_name(5) == 'triad'
    assert tonalitytools.chord_class_extent_to_extent_name(7) == 'seventh'
    assert tonalitytools.chord_class_extent_to_extent_name(9) == 'ninth'
    assert tonalitytools.chord_class_extent_to_extent_name(11) == 'eleventh'
    assert tonalitytools.chord_class_extent_to_extent_name(13) == 'thirteenth'


def test_tonalitytools_chord_class_extent_to_extent_name_02():

    assert py.test.raises(TonalHarmonyError,
        'tonalitytools.chord_class_extent_to_extent_name(1)')
