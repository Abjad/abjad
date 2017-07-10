# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Measure__get_likely_multiplier_of_components_01():
    r'''Components were likely multiplied by 5/4.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.mutate(staff).scale(abjad.Multiplier(5, 4))
    assert abjad.Measure._get_likely_multiplier_of_components(staff[:]) == \
        abjad.Multiplier(5, 4)


def test_scoretools_Measure__get_likely_multiplier_of_components_02():
    r'''Components were likely multiplied by 3/2.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.mutate(staff).scale(abjad.Multiplier(3, 2))
    assert abjad.Measure._get_likely_multiplier_of_components(staff[:]) == \
        abjad.Multiplier(3, 2)


def test_scoretools_Measure__get_likely_multiplier_of_components_03():
    r'''Components were likely multiplied by 7/4.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.mutate(staff).scale(abjad.Multiplier(7, 4))
    assert abjad.Measure._get_likely_multiplier_of_components(staff[:]) == \
        abjad.Multiplier(7, 4)


def test_scoretools_Measure__get_likely_multiplier_of_components_04():
    r'''Components likely multiplier not recoverable.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.mutate(staff).scale(abjad.Multiplier(2))
    assert abjad.Measure._get_likely_multiplier_of_components(staff[:]) == \
        abjad.Multiplier(1)


def test_scoretools_Measure__get_likely_multiplier_of_components_05():
    r'''Components likely multiplier not recoverable.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.mutate(staff).scale(abjad.Multiplier(1, 2))
    assert abjad.Measure._get_likely_multiplier_of_components(staff[:]) == \
        abjad.Multiplier(1)


def test_scoretools_Measure__get_likely_multiplier_of_components_06():
    r'''Components multiplier recoverable only to within one power of two.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.mutate(staff).scale(abjad.Multiplier(10, 4))
    assert not abjad.Measure._get_likely_multiplier_of_components(staff[:]) == \
        abjad.Multiplier(10, 4)
    assert abjad.Measure._get_likely_multiplier_of_components(staff[:]) == \
        abjad.Multiplier(5, 4)


def test_scoretools_Measure__get_likely_multiplier_of_components_07():
    r'''Returns none when more than one likely multiplier.
    '''

    maker = abjad.NoteMaker()
    notes = maker([0], [(1, 8), (7, 32)])
    staff = abjad.Staff(notes)
    assert abjad.Measure._get_likely_multiplier_of_components(staff[:]) is None
