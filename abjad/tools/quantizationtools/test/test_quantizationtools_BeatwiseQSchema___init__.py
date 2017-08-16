import abjad
from abjad.tools import quantizationtools


def test_quantizationtools_BeatwiseQSchema___init___01():

    item_a = abjad.quantizationtools.BeatwiseQSchemaItem(
        search_tree=abjad.quantizationtools.UnweightedSearchTree({2: None}))
    item_b = abjad.quantizationtools.BeatwiseQSchemaItem(tempo=((1, 4), 76))
    item_c = abjad.quantizationtools.BeatwiseQSchemaItem(beatspan=(1, 8))

    schema = abjad.quantizationtools.BeatwiseQSchema(
        {2: item_a, 4: item_b, 7: item_c},
        beatspan=abjad.Duration(1, 32),
        search_tree=abjad.quantizationtools.UnweightedSearchTree({3: None}),
        tempo=abjad.MetronomeMark((1, 16), 32)
        )

    assert len(schema.items) == 3
    assert schema.beatspan == abjad.Duration(1, 32)
    assert schema.search_tree == quantizationtools.UnweightedSearchTree({3: None})
    assert schema.tempo == abjad.MetronomeMark((1, 16), 32)


def test_quantizationtools_BeatwiseQSchema___init___02():

    schema = abjad.quantizationtools.BeatwiseQSchema()

    assert len(schema.items) == 0
    assert schema.beatspan == abjad.Duration(1, 4)
    assert schema.search_tree == quantizationtools.UnweightedSearchTree()
    assert schema.tempo == abjad.MetronomeMark((1, 4), 60)
