from abjad import *


def test_resttools_make_repeated_rests_from_time_signature_01():
    '''Make repeated rests from integer pair.
    '''

    rests = resttools.make_repeated_rests_from_time_signature((5, 32))
    staff = Staff(rests)

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == '\\new Staff {\n\tr32\n\tr32\n\tr32\n\tr32\n\tr32\n}'


def test_resttools_make_repeated_rests_from_time_signature_02():
    '''Make repeated rests from time signature.
    '''

    time_signature = contexttools.TimeSignatureMark((5, 32))
    rests = resttools.make_repeated_rests_from_time_signature(time_signature)
    staff = Staff(rests)

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == '\\new Staff {\n\tr32\n\tr32\n\tr32\n\tr32\n\tr32\n}'
