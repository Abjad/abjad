from abjad import *


def test_TimeSignatureMark_storage_format_01():

    time_signature_mark = contexttools.TimeSignatureMark((3, 16), partial=Duration(1, 16))

    r'''
    contexttools.TimeSignatureMark(
        (3, 16),
        partial=durationtools.Duration(1, 16)
    )
    '''

    assert time_signature_mark.storage_format == 'contexttools.TimeSignatureMark(\n\t(3, 16),\n\tpartial=durationtools.Duration(1, 16)\n\t)'
