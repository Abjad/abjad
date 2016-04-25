# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_TypedOrderedDict___eq___01():

    dictionary_1 = datastructuretools.TypedOrderedDict([
        ('flavor', 'cherry'), ('count', 2),
        ])
    dictionary_2 = datastructuretools.TypedOrderedDict([
        ('flavor', 'cherry'), ('count', 2),
        ])
    dictionary_3 = datastructuretools.TypedOrderedDict([
        ('flavor', 'chocolate'), ('count', 2),
        ])

    assert dictionary_1 == dictionary_1
    assert dictionary_1 == dictionary_2
    assert not dictionary_1 == dictionary_3
    assert dictionary_2 == dictionary_1
    assert dictionary_2 == dictionary_2
    assert not dictionary_2 == dictionary_3
    assert not dictionary_3 == dictionary_1
    assert not dictionary_3 == dictionary_2
    assert dictionary_3 == dictionary_3


def test_datastructuretools_TypedOrderedDict___eq___02():

    dictionary_1 = datastructuretools.TypedOrderedDict([
        ('flavor', 'cherry'), ('count', 2),
        ])
    dictionary_2 = datastructuretools.TypedOrderedDict([
        ('flavor', 'cherry'), ('count', 2), ('color', 'red'),
        ])

    assert dictionary_1 == dictionary_1
    assert not dictionary_1 == dictionary_2
    assert not dictionary_2 == dictionary_1
    assert dictionary_2 == dictionary_2
