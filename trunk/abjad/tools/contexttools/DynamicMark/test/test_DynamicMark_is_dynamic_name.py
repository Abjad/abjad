from abjad import *


def test_DynamicMark_is_dynamic_name_01():

    assert contexttools.DynamicMark.is_dynamic_name('ff')
    assert contexttools.DynamicMark.is_dynamic_name('f')
    assert contexttools.DynamicMark.is_dynamic_name('p')
    assert contexttools.DynamicMark.is_dynamic_name('pp')


def test_DynamicMark_is_dynamic_name_02():

    assert not contexttools.DynamicMark.is_dynamic_name('x')
