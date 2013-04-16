from experimental.tools.scoremanagementtools import specifiers
from experimental import *


def test_MusicContributionSpecifier___eq___01():

    specifier_1 = scoremanagementtools.specifiers.MusicContributionSpecifier([])
    specifier_1.append(specifiers.ArticulationSpecifier(articulation_handler_name='foo'))

    specifier_2 = scoremanagementtools.specifiers.MusicContributionSpecifier([])
    specifier_2.append(specifiers.ArticulationSpecifier(articulation_handler_name='foo'))

    specifier_3 = scoremanagementtools.specifiers.MusicContributionSpecifier([])

    assert specifier_1 == specifier_1
    assert specifier_1 == specifier_2
    assert not specifier_1 == specifier_3
    assert specifier_2 == specifier_1
    assert specifier_2 == specifier_2
    assert not specifier_2 == specifier_3
    assert not specifier_3 == specifier_1
    assert not specifier_3 == specifier_2
    assert specifier_3 == specifier_3
