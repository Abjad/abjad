# -*- encoding: utf-8 -*-
from abjad import *


def test_DynamicMark_dynamic_name_01():
    r'''Dynamic name is read / write.
    '''

    dynamic = Dynamic('f')
    assert dynamic.dynamic_name == 'f'

    dynamic.dynamic_name = 'p'
    assert dynamic.dynamic_name == 'p'
