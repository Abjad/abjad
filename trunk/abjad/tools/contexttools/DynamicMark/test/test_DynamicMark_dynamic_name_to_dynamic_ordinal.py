from abjad import *


def test_DynamicMark_dynamic_name_to_dynamic_ordinal_01():

    assert contexttools.DynamicMark.dynamic_name_to_dynamic_ordinal('pp') == -3
    assert contexttools.DynamicMark.dynamic_name_to_dynamic_ordinal('p') == -2
    assert contexttools.DynamicMark.dynamic_name_to_dynamic_ordinal('mp') == -1
    assert contexttools.DynamicMark.dynamic_name_to_dynamic_ordinal('mf') == 1
    assert contexttools.DynamicMark.dynamic_name_to_dynamic_ordinal('f') == 2
    assert contexttools.DynamicMark.dynamic_name_to_dynamic_ordinal('ff') == 3


def test_DynamicMark_dynamic_name_to_dynamic_ordinal_02():

    assert contexttools.DynamicMark.dynamic_name_to_dynamic_ordinal('fp') == -2
    assert contexttools.DynamicMark.dynamic_name_to_dynamic_ordinal('sf') == 2
    assert contexttools.DynamicMark.dynamic_name_to_dynamic_ordinal('sff') == 3
    assert contexttools.DynamicMark.dynamic_name_to_dynamic_ordinal('sp') == -2
    assert contexttools.DynamicMark.dynamic_name_to_dynamic_ordinal('sfz') == 2
