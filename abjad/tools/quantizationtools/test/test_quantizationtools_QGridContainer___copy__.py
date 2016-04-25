# -*- coding: utf-8 -*-
import copy
from abjad import *


def test_quantizationtools_QGridContainer___copy___01():

    tree = quantizationtools.QGridContainer(
        preprolated_duration=1,
        children=[
            quantizationtools.QGridLeaf(preprolated_duration=1),
            quantizationtools.QGridContainer(
                preprolated_duration=2,
                children=[
                    quantizationtools.QGridLeaf(preprolated_duration=3),
                    quantizationtools.QGridContainer(
                        preprolated_duration=4,
                        children=[
                            quantizationtools.QGridLeaf(preprolated_duration=1),
                            quantizationtools.QGridLeaf(preprolated_duration=1),
                            quantizationtools.QGridLeaf(preprolated_duration=1)
                        ])
                ]),
            quantizationtools.QGridLeaf(preprolated_duration=2)
        ])

    copied = copy.copy(tree)

    assert format(tree) == format(copied)
    assert tree is not copied
    assert tree[0] is not copied[0]
    assert tree[1] is not copied[1]
    assert tree[2] is not copied[2]
