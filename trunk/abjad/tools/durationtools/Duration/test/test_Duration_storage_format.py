from abjad import *


def test_Duration_storage_format_01():

    assert Duration(1, 4).storage_format == 'durationtools.Duration(1, 4)'
