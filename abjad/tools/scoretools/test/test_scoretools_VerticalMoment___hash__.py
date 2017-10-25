import abjad


def test_scoretools_VerticalMoment___hash___01():
    r'''Vertical moments behave well when included in a set.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    vms = []
    vms.extend(abjad.iterate(staff).vertical_moments())
    vms.extend(abjad.iterate(staff).vertical_moments())

    assert len(vms) == 8
    assert len(set(vms)) == 4
