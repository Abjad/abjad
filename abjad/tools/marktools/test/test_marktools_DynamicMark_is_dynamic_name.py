# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_DynamicMark_is_dynamic_name_01():

    assert marktools.DynamicMark.is_dynamic_name('ff')
    assert marktools.DynamicMark.is_dynamic_name('f')
    assert marktools.DynamicMark.is_dynamic_name('p')
    assert marktools.DynamicMark.is_dynamic_name('pp')


def test_marktools_DynamicMark_is_dynamic_name_02():

    assert not marktools.DynamicMark.is_dynamic_name('x')
