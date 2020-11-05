import abjad


def test_get_has_effective_indicator_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.attach("foo", staff[2], context="Staff")

    assert not abjad.get.has_effective_indicator(staff, str)
    assert not abjad.get.has_effective_indicator(staff[0], str)
    assert not abjad.get.has_effective_indicator(staff[1], str)
    assert abjad.get.has_effective_indicator(staff[2], str)
    assert abjad.get.has_effective_indicator(staff[3], str)
