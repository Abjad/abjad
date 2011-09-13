from abjad import *


def test_DynamicMark_dynamic_ordinal_to_dynamic_name_01():

    assert contexttools.DynamicMark.dynamic_ordinal_to_dynamic_name(-3) == 'pp'
    assert contexttools.DynamicMark.dynamic_ordinal_to_dynamic_name(-2) == 'p'
    assert contexttools.DynamicMark.dynamic_ordinal_to_dynamic_name(-1) == 'mp'
    assert contexttools.DynamicMark.dynamic_ordinal_to_dynamic_name(1) == 'mf'
    assert contexttools.DynamicMark.dynamic_ordinal_to_dynamic_name(2) == 'f'
    assert contexttools.DynamicMark.dynamic_ordinal_to_dynamic_name(3) == 'ff'
