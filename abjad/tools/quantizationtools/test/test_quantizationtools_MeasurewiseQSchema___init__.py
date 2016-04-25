# -*- coding: utf-8 -*-
from abjad import *


def test_quantizationtools_MeasurewiseQSchema___init___01():

    item_a = quantizationtools.MeasurewiseQSchemaItem(search_tree=quantizationtools.UnweightedSearchTree({2: None}))
    item_b = quantizationtools.MeasurewiseQSchemaItem(tempo=((1, 4), 76))
    item_c = quantizationtools.MeasurewiseQSchemaItem(time_signature=(3, 4))
    item_d = quantizationtools.MeasurewiseQSchemaItem(use_full_measure=True)

    schema = quantizationtools.MeasurewiseQSchema(
        {2: item_a, 4: item_b, 7: item_c, 8: item_d},
        search_tree=quantizationtools.UnweightedSearchTree({3: None}),
        tempo=((1, 8), 58),
        time_signature=(5, 8),
        use_full_measure=False,
        )

    assert len(schema.items) == 4
    assert schema.search_tree == quantizationtools.UnweightedSearchTree({3: None})
    assert schema.tempo == Tempo((1, 8), 58)
    assert schema.time_signature == TimeSignature((5, 8))
    assert schema.use_full_measure == False


def test_quantizationtools_MeasurewiseQSchema___init___02():

    schema = quantizationtools.MeasurewiseQSchema()

    assert len(schema.items) == 0
    assert schema.search_tree == quantizationtools.UnweightedSearchTree()
    assert schema.tempo == Tempo((1, 4), 60)
    assert schema.time_signature == TimeSignature((4, 4))
    assert schema.use_full_measure == False
