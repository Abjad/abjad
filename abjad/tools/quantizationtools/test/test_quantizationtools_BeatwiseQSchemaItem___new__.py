import abjad
import pytest
from abjad.tools import quantizationtools


def test_quantizationtools_BeatwiseQSchemaItem___new___01():

    item = abjad.quantizationtools.BeatwiseQSchemaItem()

    assert item.beatspan is None
    assert item.search_tree is None
    assert item.tempo is None


def test_quantizationtools_BeatwiseQSchemaItem___new___02():

    item = abjad.quantizationtools.BeatwiseQSchemaItem(
        tempo=((1, 4), 60)
        )

    assert item.beatspan is None
    assert item.search_tree is None
    assert item.tempo == abjad.MetronomeMark((1, 4), 60)


def test_quantizationtools_BeatwiseQSchemaItem___new___03():

    item = abjad.quantizationtools.BeatwiseQSchemaItem(
        beatspan=(1, 8)
        )

    assert item.beatspan == abjad.Duration(1, 8)
    assert item.search_tree is None
    assert item.tempo is None


def test_quantizationtools_BeatwiseQSchemaItem___new___04():

    item = abjad.quantizationtools.BeatwiseQSchemaItem(
        beatspan=(1, 8),
        tempo=((1, 4), 57),
        )

    assert item.beatspan == abjad.Duration(1, 8)
    assert item.search_tree is None
    assert item.tempo == abjad.MetronomeMark((1, 4), 57)


def test_quantizationtools_BeatwiseQSchemaItem___new___05():

    tempo = abjad.MetronomeMark(textual_indication='lento')
    pytest.raises(
        AssertionError, 
        'item = abjad.quantizationtools.BeatwiseQSchemaItem(tempo=tempo)',
        )
