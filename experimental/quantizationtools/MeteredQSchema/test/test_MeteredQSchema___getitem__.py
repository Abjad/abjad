from abjad.tools import contexttools
from experimental import quantizationtools


def test_MeteredQSchema___getitem___01():

    schema = quantizationtools.MeteredQSchema()

    assert schema[0] == schema[1] == schema[2] == {
        'search_tree': quantizationtools.QGridSearchTree(),
        'tempo': contexttools.TempoMark((1, 4), 60),
        'time_signature': contexttools.TimeSignatureMark((4, 4)),
        'use_full_measure': False,
    }


def test_MeteredQSchema___getitem___02():

    item_a = quantizationtools.MeteredQSchemaItem(search_tree=quantizationtools.QGridSearchTree({2: None}))
    item_b = quantizationtools.MeteredQSchemaItem(tempo=((1, 4), 76))
    item_c = quantizationtools.MeteredQSchemaItem(time_signature=(3, 4))
    item_d = quantizationtools.MeteredQSchemaItem(
        search_tree={5: None},
        use_full_measure=True
        )

    schema = quantizationtools.MeteredQSchema(
        {2: item_a, 4: item_b, 7: item_c, 8: item_d},
        search_tree=quantizationtools.QGridSearchTree({3: None}),
        tempo=((1, 8), 58),
        time_signature=(5, 8),
        use_full_measure=False,
        )

    assert schema[0] == schema[1] == {
        'search_tree': quantizationtools.QGridSearchTree({3: None}),
        'tempo': contexttools.TempoMark((1, 8), 58),
        'time_signature': contexttools.TimeSignatureMark((5, 8)),
        'use_full_measure': False,
    }

    assert schema[2] == schema[3] == {
        'search_tree': quantizationtools.QGridSearchTree({2: None}),
        'tempo': contexttools.TempoMark((1, 8), 58),
        'time_signature': contexttools.TimeSignatureMark((5, 8)),
        'use_full_measure': False,
    }

    assert schema[4] == schema[5] == schema[6] == {
        'search_tree': quantizationtools.QGridSearchTree({2: None}),
        'tempo': contexttools.TempoMark((1, 4), 76),
        'time_signature': contexttools.TimeSignatureMark((5, 8)),
        'use_full_measure': False,
    }

    assert schema[7] == {
        'search_tree': quantizationtools.QGridSearchTree({2: None}),
        'tempo': contexttools.TempoMark((1, 4), 76),
        'time_signature': contexttools.TimeSignatureMark((3, 4)),
        'use_full_measure': False,
    }

    assert schema[8] == schema[9] == schema[1000] == {
        'search_tree': quantizationtools.QGridSearchTree({5: None}),
        'tempo': contexttools.TempoMark((1, 4), 76),
        'time_signature': contexttools.TimeSignatureMark((3, 4)),
        'use_full_measure': True,
    }
