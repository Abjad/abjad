# -*- encoding: utf-8 -*-
from abjad import *


def test_TypedOrderedDict___eq___01():

    dict_1 = datastructuretools.TypedOrderedDict([
        ('flavor', 'cherry'), ('count', 2),
        ])
    dict_2 = datastructuretools.TypedOrderedDict([
        ('flavor', 'cherry'), ('count', 2),
        ])
    dict_3 = datastructuretools.TypedOrderedDict([
        ('flavor', 'chocolate'), ('count', 2),
        ])

    assert dict_1 == dict_1
    assert dict_1 == dict_2
    assert not dict_1 == dict_3
    assert dict_2 == dict_1
    assert dict_2 == dict_2
    assert not dict_2 == dict_3
    assert not dict_3 == dict_1
    assert not dict_3 == dict_2
    assert dict_3 == dict_3


def test_TypedOrderedDict___eq___02():

    dict_1 = datastructuretools.TypedOrderedDict([
        ('flavor', 'cherry'), ('count', 2),
        ])
    dict_2 = datastructuretools.TypedOrderedDict([
        ('flavor', 'cherry'), ('count', 2), ('color', 'red'),
        ])

    assert dict_1 == dict_1
    assert not dict_1 == dict_2
    assert not dict_2 == dict_1
    assert dict_2 == dict_2