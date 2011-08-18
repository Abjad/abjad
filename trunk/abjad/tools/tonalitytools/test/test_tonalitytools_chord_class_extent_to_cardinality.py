from abjad import *
from abjad.tools import tonalitytools
import py.test


def test_tonalitytools_chord_class_extent_to_cardinality_01():

    assert tonalitytools.chord_class_extent_to_cardinality(5) == 3
    assert tonalitytools.chord_class_extent_to_cardinality(7) == 4
    assert tonalitytools.chord_class_extent_to_cardinality(9) == 5
    assert tonalitytools.chord_class_extent_to_cardinality(11) == 6
    assert tonalitytools.chord_class_extent_to_cardinality(13) == 7


def test_tonalitytools_chord_class_extent_to_cardinality_02():

    assert py.test.raises(TonalHarmonyError,
        'tonalitytools.chord_class_extent_to_cardinality(1)')
