from abjad.tools import contexttools
from abjad.tools import durationtools
from experimental import quantizationtools
import py.test


def test_UnmeteredQSchemaItem___new___01():

    item = quantizationtools.UnmeteredQSchemaItem()

    assert item.beatspan is None
    assert item.search_tree is None
    assert item.tempo is None


def test_UnmeteredQSchemaItem___new___02():

    item = quantizationtools.UnmeteredQSchemaItem(
        tempo=((1, 4), 60)
        )

    assert item.beatspan is None
    assert item.search_tree is None
    assert item.tempo == contexttools.TempoMark((1, 4), 60)


def test_UnmeteredQSchemaItem___new___03():

    item = quantizationtools.UnmeteredQSchemaItem(
        beatspan=(1, 8)
        )

    assert item.beatspan == durationtools.Duration(1, 8)
    assert item.search_tree is None
    assert item.tempo is None


def test_UnmeteredQSchemaItem___new___04():

    item = quantizationtools.UnmeteredQSchemaItem(
        beatspan=(1, 8),
        tempo=((1, 4), 57),
        )

    assert item.beatspan == durationtools.Duration(1, 8)
    assert item.search_tree is None
    assert item.tempo == contexttools.TempoMark((1, 4), 57)


def test_UnmeteredQSchemaItem___new___05():

    tempo = contexttools.TempoMark('lento')
    py.test.raises('item = quantizationtools.UnmeteredQSchemaItem(tempo=tempo)')
