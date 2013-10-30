# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_DynamicMark_dynamic_ordinal_to_dynamic_name_01():

    assert marktools.DynamicMark.dynamic_ordinal_to_dynamic_name(-3) == 'pp'
    assert marktools.DynamicMark.dynamic_ordinal_to_dynamic_name(-2) == 'p'
    assert marktools.DynamicMark.dynamic_ordinal_to_dynamic_name(-1) == 'mp'
    assert marktools.DynamicMark.dynamic_ordinal_to_dynamic_name(1) == 'mf'
    assert marktools.DynamicMark.dynamic_ordinal_to_dynamic_name(2) == 'f'
    assert marktools.DynamicMark.dynamic_ordinal_to_dynamic_name(3) == 'ff'
