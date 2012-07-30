from abjad.tools import contexttools
from experimental import quantizationtools


def test_MeasurewiseQSchema___init___01():

    item_a = quantizationtools.MeasurewiseQSchemaItem(search_tree=quantizationtools.SimpleSearchTree({2: None}))
    item_b = quantizationtools.MeasurewiseQSchemaItem(tempo=((1, 4), 76))
    item_c = quantizationtools.MeasurewiseQSchemaItem(time_signature=(3, 4))
    item_d = quantizationtools.MeasurewiseQSchemaItem(use_full_measure=True)

    schema = quantizationtools.MeasurewiseQSchema(
        {2: item_a, 4: item_b, 7: item_c, 8: item_d},
        search_tree=quantizationtools.SimpleSearchTree({3: None}),
        tempo=((1, 8), 58),
        time_signature=(5, 8),
        use_full_measure=False,
        )

    assert len(schema.items) == 4
    assert schema.search_tree == quantizationtools.SimpleSearchTree({3: None})
    assert schema.tempo == contexttools.TempoMark((1, 8), 58)
    assert schema.time_signature == contexttools.TimeSignatureMark((5, 8))
    assert schema.use_full_measure == False


def test_MeasurewiseQSchema___init___02():

    schema = quantizationtools.MeasurewiseQSchema()

    assert len(schema.items) == 0
    assert schema.search_tree == quantizationtools.SimpleSearchTree()
    assert schema.tempo == contexttools.TempoMark((1, 4), 60)
    assert schema.time_signature == contexttools.TimeSignatureMark((4, 4))
    assert schema.use_full_measure == False
