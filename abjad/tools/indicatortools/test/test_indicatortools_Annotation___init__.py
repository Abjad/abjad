# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_Annotation___init___01():
    r'''Initializes annotation with dictionary.
    '''

    annotation = indicatortools.Annotation('special dictionary', {})
    assert isinstance(annotation, indicatortools.Annotation)


def test_indicatortools_Annotation___init___02():
    r'''Initializes annotation with only one argument.
    '''

    annotation = indicatortools.Annotation('foo')
    assert isinstance(annotation, indicatortools.Annotation)


def test_indicatortools_Annotation___init___03():
    r'''Initializes annotation from other annotation.
    '''

    annotation_1 = indicatortools.Annotation('foo', 'bar')
    annotation_2 = indicatortools.Annotation(annotation_1)

    assert annotation_1 == annotation_2
    assert annotation_1 is not annotation_2
