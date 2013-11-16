# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_indicatortools_Annotation___setattr___01():
    r'''Slots constrain annotation attributes.
    '''

    annotation = indicatortools.Annotation('foo')

    assert pytest.raises(AttributeError, "annotation.foo = 'bar'")
