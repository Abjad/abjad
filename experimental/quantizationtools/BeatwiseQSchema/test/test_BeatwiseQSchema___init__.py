from abjad.tools import contexttools
from abjad.tools import durationtools
from experimental import quantizationtools


def test_BeatwiseQSchema___init___01():

    item_a = quantizationtools.BeatwiseQSchemaItem(
        search_tree=quantizationtools.UnweightedSearchTree({2: None}))
    item_b = quantizationtools.BeatwiseQSchemaItem(tempo=((1, 4), 76))
    item_c = quantizationtools.BeatwiseQSchemaItem(beatspan=(1, 8))

    schema = quantizationtools.BeatwiseQSchema(
        {2: item_a, 4: item_b, 7: item_c},
        beatspan=durationtools.Duration(1, 32),
        search_tree=quantizationtools.UnweightedSearchTree({3: None}),
        tempo=contexttools.TempoMark((1, 16), 32)
        )

    assert len(schema.items) == 3
    assert schema.beatspan == durationtools.Duration(1, 32)
    assert schema.search_tree == quantizationtools.UnweightedSearchTree({3: None})
    assert schema.tempo == contexttools.TempoMark((1, 16), 32)


def test_BeatwiseQSchema___init___02():

    schema = quantizationtools.BeatwiseQSchema()

    assert len(schema.items) == 0
    assert schema.beatspan == durationtools.Duration(1, 4)
    assert schema.search_tree == quantizationtools.UnweightedSearchTree()
    assert schema.tempo == contexttools.TempoMark((1, 4), 60)

