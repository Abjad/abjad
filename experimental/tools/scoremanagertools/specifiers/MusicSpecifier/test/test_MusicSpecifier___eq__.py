from experimental.tools.scoremanagertools import specifiers
from experimental import *


def test_MusicSpecifier___eq___01():

    mcs_1 = scoremanagertools.specifiers.MusicContributionSpecifier([])
    mcs_1.append(specifiers.ArticulationSpecifier(articulation_handler_name='foo articulations'))

    mcs_2 = scoremanagertools.specifiers.MusicContributionSpecifier([])
    mcs_2.append(specifiers.ArticulationSpecifier(articulation_handler_name='bar articulations'))

    ms_1 = scoremanagertools.specifiers.MusicSpecifier([mcs_1, mcs_2])

    mcs_3 = scoremanagertools.specifiers.MusicContributionSpecifier([])
    mcs_3.append(specifiers.ArticulationSpecifier(articulation_handler_name='foo articulations'))

    mcs_4 = scoremanagertools.specifiers.MusicContributionSpecifier([])
    mcs_4.append(specifiers.ArticulationSpecifier(articulation_handler_name='bar articulations'))

    ms_2 = scoremanagertools.specifiers.MusicSpecifier([mcs_3, mcs_4])

    ms_3 = scoremanagertools.specifiers.MusicSpecifier([])

    assert ms_1 == ms_1
    assert ms_1 == ms_2
    assert not ms_1 == ms_3
    assert ms_2 == ms_1
    assert ms_2 == ms_2
    assert not ms_2 == ms_3
    assert not ms_3 == ms_1
    assert not ms_3 == ms_2
    assert ms_3 == ms_3
