# -*- encoding: utf-8 -*-
from abjad import *


def test_DynamicMark_dynamic_ordinal_to_dynamic_name_01():

    assert DynamicMark.dynamic_ordinal_to_dynamic_name(-3) == 'pp'
    assert DynamicMark.dynamic_ordinal_to_dynamic_name(-2) == 'p'
    assert DynamicMark.dynamic_ordinal_to_dynamic_name(-1) == 'mp'
    assert DynamicMark.dynamic_ordinal_to_dynamic_name(1) == 'mf'
    assert DynamicMark.dynamic_ordinal_to_dynamic_name(2) == 'f'
    assert DynamicMark.dynamic_ordinal_to_dynamic_name(3) == 'ff'
