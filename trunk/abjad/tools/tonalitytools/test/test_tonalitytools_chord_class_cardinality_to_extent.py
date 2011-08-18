from abjad import *
from abjad.tools import tonalitytools
import py.test


def test_tonalitytools_chord_class_cardinality_to_extent_01():

    assert tonalitytools.chord_class_cardinality_to_extent(3) == 5
    assert tonalitytools.chord_class_cardinality_to_extent(4) == 7
    assert tonalitytools.chord_class_cardinality_to_extent(5) == 9
    assert tonalitytools.chord_class_cardinality_to_extent(6) == 11
    assert tonalitytools.chord_class_cardinality_to_extent(7) == 13


def test_tonalitytools_chord_class_cardinality_to_extent_02():

    assert py.test.raises(TonalHarmonyError,
        'tonalitytools.chord_class_cardinality_to_extent(1)')

    assert py.test.raises(TonalHarmonyError,
        'tonalitytools.chord_class_cardinality_to_extent(10)')
