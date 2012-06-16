from abjad import *


def test_durationtools_Duration_storage_format_01():

    assert Duration(1, 4).storage_format == 'durationtools.Duration(\n\t1,\n\t4\n\t)'

    r'''
    durationtools.Duration(
        1,
        4
        )
    '''
