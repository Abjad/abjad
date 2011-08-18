from abjad import *


def test_skiptools_make_repeated_skips_from_time_signature_01():
    '''Make repeated skips from integer pair.
    '''

    skips = skiptools.make_repeated_skips_from_time_signature((5, 32))
    staff = Staff(skips)

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == '\\new Staff {\n\ts32\n\ts32\n\ts32\n\ts32\n\ts32\n}'


def test_skiptools_make_repeated_skips_from_time_signature_02():
    '''Make repeated skips from time signature.
    '''

    time_signature = contexttools.TimeSignatureMark((5, 32))
    skips = skiptools.make_repeated_skips_from_time_signature(time_signature)
    staff = Staff(skips)

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == '\\new Staff {\n\ts32\n\ts32\n\ts32\n\ts32\n\ts32\n}'
