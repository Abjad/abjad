from abjad.tools import contexttools
from experimental import quantizationtools


def test_MeteredQSchema___init___01():

    item_a = quantizationtools.MeteredQSchemaItem(search_tree=quantizationtools.QGridSearchTree({2: None}))
    item_b = quantizationtools.MeteredQSchemaItem(tempo=((1, 4), 76))
    item_c = quantizationtools.MeteredQSchemaItem(time_signature=(3, 4))
    item_d = quantizationtools.MeteredQSchemaItem(use_full_measure=True)

    schema = quantizationtools.MeteredQSchema(
        {2: item_a, 4: item_b, 7: item_c, 8: item_d},
        search_tree=quantizationtools.QGridSearchTree({3: None}),
        tempo=((1, 8), 58),
        time_signature=(5, 8),
        use_full_measure=False,
        )

    assert len(schema.items) == 4
    assert schema.search_tree == quantizationtools.QGridSearchTree({3: None})
    assert schema.tempo == contexttools.TempoMark((1, 8), 58)
    assert schema.time_signature == contexttools.TimeSignatureMark((5, 8))
    assert schema.use_full_measure == False
