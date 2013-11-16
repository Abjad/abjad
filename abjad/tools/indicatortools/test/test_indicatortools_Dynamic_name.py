# -*- encoding: utf-8 -*-
from abjad import *


def test_indicatortools_Dynamic_name_01():
    r'''Dynamic name is read / write.
    '''

    dynamic = Dynamic('f')
    assert dynamic.name == 'f'

    dynamic.name = 'p'
    assert dynamic.name == 'p'
