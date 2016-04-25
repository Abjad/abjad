# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_Dynamic_composite_dynamic_name_to_steady_state_dynamic_name_01():

    dynamic = Dynamic
    assert dynamic.composite_dynamic_name_to_steady_state_dynamic_name('sfp') == 'p'
    assert dynamic.composite_dynamic_name_to_steady_state_dynamic_name('sf') == 'f'
    assert dynamic.composite_dynamic_name_to_steady_state_dynamic_name('sfz') == 'f'
    assert dynamic.composite_dynamic_name_to_steady_state_dynamic_name('fp') == 'p'
