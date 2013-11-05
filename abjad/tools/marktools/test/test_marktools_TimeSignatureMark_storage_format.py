# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_TimeSignatureMark_storage_format_01():

    time_signature_mark = marktools.TimeSignatureMark((3, 16), partial=Duration(1, 16))

    r'''
    marktools.TimeSignatureMark(
        (3, 16),
        partial=durationtools.Duration(1, 16)
    )
    '''

    assert time_signature_mark.storage_format == 'marktools.TimeSignatureMark(\n\t(3, 16),\n\tpartial=durationtools.Duration(1, 16)\n\t)'
