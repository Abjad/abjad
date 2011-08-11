from abjad import *


def test_DynamicMark_dynamic_name_string_01( ):
    '''Dynamic name string is read / write.
    '''

    dynamic = contexttools.DynamicMark('f')
    assert dynamic.dynamic_name_string == 'f'

    dynamic.dynamic_name_string = 'p'
    assert dynamic.dynamic_name_string == 'p'


