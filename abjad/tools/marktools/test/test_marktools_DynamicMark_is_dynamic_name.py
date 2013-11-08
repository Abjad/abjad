# -*- encoding: utf-8 -*-
from abjad import *


def test_DynamicMark_is_dynamic_name_01():

    assert DynamicMark.is_dynamic_name('ff')
    assert DynamicMark.is_dynamic_name('f')
    assert DynamicMark.is_dynamic_name('p')
    assert DynamicMark.is_dynamic_name('pp')


def test_DynamicMark_is_dynamic_name_02():

    assert not DynamicMark.is_dynamic_name('x')
