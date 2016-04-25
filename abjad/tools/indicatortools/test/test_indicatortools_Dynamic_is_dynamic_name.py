# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_Dynamic_is_dynamic_name_01():

    assert Dynamic.is_dynamic_name('ff')
    assert Dynamic.is_dynamic_name('f')
    assert Dynamic.is_dynamic_name('p')
    assert Dynamic.is_dynamic_name('pp')


def test_indicatortools_Dynamic_is_dynamic_name_02():

    assert not Dynamic.is_dynamic_name('x')
