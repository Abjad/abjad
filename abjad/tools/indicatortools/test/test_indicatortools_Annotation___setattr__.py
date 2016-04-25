# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_indicatortools_Annotation___setattr___01():
    r'''Slots constrain annotation attributes.
    '''

    annotation = indicatortools.Annotation('foo')

    assert pytest.raises(AttributeError, "annotation.foo = 'bar'")
