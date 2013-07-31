# -*- encoding: utf-8 -*-
from abjad import *


def test_Annotation___init___01():
    r'''Initialize annotation with dictionary.
    '''

    annotation = marktools.Annotation('special dictionary', {})
    assert isinstance(annotation, marktools.Annotation)


def test_Annotation___init___02():
    r'''Initialize annotation with only one argument.
    '''

    annotation = marktools.Annotation('foo')
    assert isinstance(annotation, marktools.Annotation)


def test_Annotation___init___03():
    r'''Initialize annotation from other annotation.
    '''

    annotation_1 = marktools.Annotation('foo', 'bar')
    annotation_2 = marktools.Annotation(annotation_1)

    assert annotation_1 == annotation_2
    assert annotation_1 is not annotation_2
