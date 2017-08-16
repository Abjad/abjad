import abjad
import pytest
from abjad.tools import quantizationtools


def test_quantizationtools_MeasurewiseQSchemaItem___new___01():

    item = quantizationtools.MeasurewiseQSchemaItem()

    assert item.beatspan is None
    assert item.search_tree is None
    assert item.tempo is None
    assert item.time_signature is None


def test_quantizationtools_MeasurewiseQSchemaItem___new___02():

    item = quantizationtools.MeasurewiseQSchemaItem(
        tempo=((1, 4), 60)
        )

    assert item.beatspan is None
    assert item.search_tree is None
    assert item.tempo == abjad.MetronomeMark((1, 4), 60)
    assert item.time_signature is None


def test_quantizationtools_MeasurewiseQSchemaItem___new___03():

    item = quantizationtools.MeasurewiseQSchemaItem(
        time_signature=(6, 8)
        )

    assert item.beatspan == abjad.Duration(1, 8)
    assert item.search_tree is None
    assert item.tempo is None
    assert item.time_signature == abjad.TimeSignature((6, 8))


def test_quantizationtools_MeasurewiseQSchemaItem___new___04():

    item = quantizationtools.MeasurewiseQSchemaItem(
        tempo=((1, 4), 57),
        time_signature=(6, 8),
        )

    assert item.beatspan == abjad.Duration(1, 8)
    assert item.search_tree is None
    assert item.tempo == abjad.MetronomeMark((1, 4), 57)
    assert item.time_signature == abjad.TimeSignature((6, 8))


def test_quantizationtools_MeasurewiseQSchemaItem___new___05():

    tempo = abjad.MetronomeMark(textual_indication='lento')
    pytest.raises(
        AssertionError,
        'item = quantizationtools.MeasurewiseQSchemaItem(tempo=tempo)',
        )
