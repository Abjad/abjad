# -*- coding: utf-8 -*-
from abjad import *


def test_quantizationtools_MeasurewiseQSchema___getitem___01():

    schema = quantizationtools.MeasurewiseQSchema()

    assert schema[0] == schema[1] == schema[2] == {
        'search_tree': quantizationtools.UnweightedSearchTree(),
        'tempo': Tempo((1, 4), 60),
        'time_signature': TimeSignature((4, 4)),
        'use_full_measure': False,
    }


def test_quantizationtools_MeasurewiseQSchema___getitem___02():

    item_a = quantizationtools.MeasurewiseQSchemaItem(search_tree=quantizationtools.UnweightedSearchTree({2: None}))
    item_b = quantizationtools.MeasurewiseQSchemaItem(tempo=((1, 4), 76))
    item_c = quantizationtools.MeasurewiseQSchemaItem(time_signature=(3, 4))
    item_d = quantizationtools.MeasurewiseQSchemaItem(
        search_tree=quantizationtools.UnweightedSearchTree({5: None}),
        use_full_measure=True
        )

    schema = quantizationtools.MeasurewiseQSchema(
        {2: item_a, 4: item_b, 7: item_c, 8: item_d},
        search_tree=quantizationtools.UnweightedSearchTree({3: None}),
        tempo=((1, 8), 58),
        time_signature=(5, 8),
        use_full_measure=False,
        )

    assert schema[0] == schema[1] == {
        'search_tree': quantizationtools.UnweightedSearchTree({3: None}),
        'tempo': Tempo((1, 8), 58),
        'time_signature': TimeSignature((5, 8)),
        'use_full_measure': False,
    }

    assert schema[2] == schema[3] == {
        'search_tree': quantizationtools.UnweightedSearchTree({2: None}),
        'tempo': Tempo((1, 8), 58),
        'time_signature': TimeSignature((5, 8)),
        'use_full_measure': False,
    }

    assert schema[4] == schema[5] == schema[6] == {
        'search_tree': quantizationtools.UnweightedSearchTree({2: None}),
        'tempo': Tempo((1, 4), 76),
        'time_signature': TimeSignature((5, 8)),
        'use_full_measure': False,
    }

    assert schema[7] == {
        'search_tree': quantizationtools.UnweightedSearchTree({2: None}),
        'tempo': Tempo((1, 4), 76),
        'time_signature': TimeSignature((3, 4)),
        'use_full_measure': False,
    }

    assert schema[8] == schema[9] == schema[1000] == {
        'search_tree': quantizationtools.UnweightedSearchTree({5: None}),
        'tempo': Tempo((1, 4), 76),
        'time_signature': TimeSignature((3, 4)),
        'use_full_measure': True,
    }
