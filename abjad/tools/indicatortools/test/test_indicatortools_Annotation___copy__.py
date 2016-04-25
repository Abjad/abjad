# -*- coding: utf-8 -*-
import copy
from abjad import *


def test_indicatortools_Annotation___copy___01():
    r'''Annotation copy copies annotation contents.
    '''

    dictionary = {}
    annotation_1 = indicatortools.Annotation('special dictionary', dictionary)
    annotation_2 = copy.copy(annotation_1)
    assert annotation_1 == annotation_2
    assert annotation_1 is not annotation_2
    assert annotation_1.name == annotation_2.name == 'special dictionary'
    assert annotation_1.value == annotation_2.value == dictionary
    assert annotation_1.value is not annotation_2.value is not dictionary
