from abjad import *


def test_DynamicMark_dynamic_name_01():
    '''Dynamic name is read / write.
    '''

    dynamic = contexttools.DynamicMark('f')
    assert dynamic.dynamic_name == 'f'

    dynamic.dynamic_name = 'p'
    assert dynamic.dynamic_name == 'p'
