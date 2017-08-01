# -*- coding: utf-8 -*-
import copy
import abjad


def test_datastructuretools_TypedOrderedDict___deepcopy___01():

    dictionary_1 = abjad.TypedOrderedDict([
        ('flavor', 'cherry'), ('count', 2),
        ])
    dictionary_2 = copy.deepcopy(dictionary_1)

    assert dictionary_1 == dictionary_2
    assert repr(dictionary_1) == repr(dictionary_2)
