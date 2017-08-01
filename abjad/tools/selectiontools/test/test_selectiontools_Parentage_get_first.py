# -*- coding: utf-8 -*-
import abjad


def test_selectiontools_Parentage_get_first_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")

    for leaf in staff:
        assert abjad.inspect(leaf).get_parentage().get_first(abjad.Staff) is staff

    assert abjad.inspect(staff).get_parentage(include_self=True).get_first(abjad.Staff) is staff
    assert abjad.inspect(staff).get_parentage(include_self=False).get_first(abjad.Staff) is None
