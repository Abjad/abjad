from abjad.tools import contexttools
from abjad.tools import durationtools
from experimental import quantizationtools
import py.test


def test_MeteredQSchemaItem___new___01():

    item = quantizationtools.MeteredQSchemaItem()

    assert item.beatspan is None
    assert item.search_tree is None
    assert item.tempo is None
    assert item.time_signature is None


def test_MeteredQSchemaItem___new___02():

    item = quantizationtools.MeteredQSchemaItem(
        tempo=((1, 4), 60)
        )

    assert item.beatspan is None
    assert item.search_tree is None
    assert item.tempo == contexttools.TempoMark((1, 4), 60)
    assert item.time_signature is None


def test_MeteredQSchemaItem___new___03():

    item = quantizationtools.MeteredQSchemaItem(
        time_signature=(6, 8)
        )

    assert item.beatspan == durationtools.Duration(1, 8)
    assert item.search_tree is None
    assert item.tempo is None
    assert item.time_signature == contexttools.TimeSignatureMark((6, 8))


def test_MeteredQSchemaItem___new___04():

    item = quantizationtools.MeteredQSchemaItem(
        tempo=((1, 4), 57),
        time_signature=(6, 8),
        )

    assert item.beatspan == durationtools.Duration(1, 8)
    assert item.search_tree is None
    assert item.tempo == contexttools.TempoMark((1, 4), 57)
    assert item.time_signature == contexttools.TimeSignatureMark((6, 8))


def test_MeteredQSchemaItem___new___05():

    tempo = contexttools.TempoMark('lento')
    py.test.raises('item = quantizationtools.MeteredQSchemaItem(tempo=tempo)')
