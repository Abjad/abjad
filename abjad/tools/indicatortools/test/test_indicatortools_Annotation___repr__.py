# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.indicatortools import Annotation


def test_indicatortools_Annotation___repr___01():
    r'''Repr of unattached annotation is evaluable.
    '''

    annotation_1 = indicatortools.Annotation('foo')
    annotation_2 = eval(repr(annotation_1))

    assert isinstance(annotation_1, indicatortools.Annotation)
    assert isinstance(annotation_2, indicatortools.Annotation)
    assert annotation_1 == annotation_2
