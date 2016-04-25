# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Measure__get_likely_multiplier_of_components_01():
    r'''Components were likely multiplied by 5/4.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    mutate(staff).scale(Multiplier(5, 4))
    assert Measure._get_likely_multiplier_of_components(staff[:]) == \
        Multiplier(5, 4)


def test_scoretools_Measure__get_likely_multiplier_of_components_02():
    r'''Components were likely multiplied by 3/2.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    mutate(staff).scale(Multiplier(3, 2))
    assert Measure._get_likely_multiplier_of_components(staff[:]) == \
        Multiplier(3, 2)


def test_scoretools_Measure__get_likely_multiplier_of_components_03():
    r'''Components were likely multiplied by 7/4.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    mutate(staff).scale(Multiplier(7, 4))
    assert Measure._get_likely_multiplier_of_components(staff[:]) == \
        Multiplier(7, 4)


def test_scoretools_Measure__get_likely_multiplier_of_components_04():
    r'''Components likely multiplier not recoverable.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    mutate(staff).scale(Multiplier(2))
    assert Measure._get_likely_multiplier_of_components(staff[:]) == \
        Multiplier(1)


def test_scoretools_Measure__get_likely_multiplier_of_components_05():
    r'''Components likely multiplier not recoverable.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    mutate(staff).scale(Multiplier(1, 2))
    assert Measure._get_likely_multiplier_of_components(staff[:]) == \
        Multiplier(1)


def test_scoretools_Measure__get_likely_multiplier_of_components_06():
    r'''Components multiplier recoverable only to within one power of two.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    mutate(staff).scale(Multiplier(10, 4))
    assert not Measure._get_likely_multiplier_of_components(staff[:]) == \
        Multiplier(10, 4)
    assert Measure._get_likely_multiplier_of_components(staff[:]) == \
        Multiplier(5, 4)


def test_scoretools_Measure__get_likely_multiplier_of_components_07():
    r'''Returns none when more than one likely multiplier.
    '''

    staff = Staff(scoretools.make_notes([0], [(1, 8), (7, 32)]))
    assert Measure._get_likely_multiplier_of_components(staff[:]) is None
