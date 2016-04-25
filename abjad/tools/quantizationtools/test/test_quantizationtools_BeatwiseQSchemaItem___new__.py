# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_quantizationtools_BeatwiseQSchemaItem___new___01():

    item = quantizationtools.BeatwiseQSchemaItem()

    assert item.beatspan is None
    assert item.search_tree is None
    assert item.tempo is None


def test_quantizationtools_BeatwiseQSchemaItem___new___02():

    item = quantizationtools.BeatwiseQSchemaItem(
        tempo=((1, 4), 60)
        )

    assert item.beatspan is None
    assert item.search_tree is None
    assert item.tempo == Tempo((1, 4), 60)


def test_quantizationtools_BeatwiseQSchemaItem___new___03():

    item = quantizationtools.BeatwiseQSchemaItem(
        beatspan=(1, 8)
        )

    assert item.beatspan == durationtools.Duration(1, 8)
    assert item.search_tree is None
    assert item.tempo is None


def test_quantizationtools_BeatwiseQSchemaItem___new___04():

    item = quantizationtools.BeatwiseQSchemaItem(
        beatspan=(1, 8),
        tempo=((1, 4), 57),
        )

    assert item.beatspan == durationtools.Duration(1, 8)
    assert item.search_tree is None
    assert item.tempo == Tempo((1, 4), 57)


def test_quantizationtools_BeatwiseQSchemaItem___new___05():

    tempo = Tempo(textual_indication='lento')
    pytest.raises(
        AssertionError, 
        'item = quantizationtools.BeatwiseQSchemaItem(tempo=tempo)',
        )
