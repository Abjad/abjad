# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
from scoremanager import specifiers


def test_MusicContributionSpecifier___eq___01():

    specifier_1 = scoremanager.specifiers.MusicContributionSpecifier([])
    specifier = specifiers.ArticulationSpecifier(
        articulation_handler_name='foo',
        )
    specifier_1.append(specifier)

    specifier_2 = scoremanager.specifiers.MusicContributionSpecifier([])
    specifier = specifiers.ArticulationSpecifier(
        articulation_handler_name='foo',
        )
    specifier_2.append(specifier)

    specifier_3 = scoremanager.specifiers.MusicContributionSpecifier([])

    assert specifier_1 == specifier_1
    assert specifier_1 == specifier_2
    assert not specifier_1 == specifier_3
    assert specifier_2 == specifier_1
    assert specifier_2 == specifier_2
    assert not specifier_2 == specifier_3
    assert not specifier_3 == specifier_1
    assert not specifier_3 == specifier_2
    assert specifier_3 == specifier_3
