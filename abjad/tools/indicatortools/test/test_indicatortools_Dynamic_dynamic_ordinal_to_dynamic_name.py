# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_Dynamic_dynamic_ordinal_to_dynamic_name_01():

    assert Dynamic.dynamic_ordinal_to_dynamic_name(-3) == 'pp'
    assert Dynamic.dynamic_ordinal_to_dynamic_name(-2) == 'p'
    assert Dynamic.dynamic_ordinal_to_dynamic_name(-1) == 'mp'
    assert Dynamic.dynamic_ordinal_to_dynamic_name(1) == 'mf'
    assert Dynamic.dynamic_ordinal_to_dynamic_name(2) == 'f'
    assert Dynamic.dynamic_ordinal_to_dynamic_name(3) == 'ff'
