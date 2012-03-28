from abjad import *


def test_TimeSignatureMark__storage_format_01():

    time_signature_mark = contexttools.TimeSignatureMark((3, 16), partial=Duration(1, 16))

    r'''
    contexttools.TimeSignatureMark(
        (3, 16),
        partial=durationtools.Duration(
            1,
            16
            )
        )
    '''

    assert time_signature_mark._tools_package_qualified_indented_repr == 'contexttools.TimeSignatureMark(\n\t(3, 16),\n\tpartial=durationtools.Duration(\n\t\t1,\n\t\t16\n\t\t)\n\t)'
