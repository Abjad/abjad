# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools import specifiers
from experimental import *


def test_MusicSpecifier_format_01():
    r'''Empty. No keywords.
    '''

    specifier = scoremanagertools.specifiers.MusicSpecifier([])

    assert repr(specifier) == 'MusicSpecifier([])'
    assert specifier._storage_format == 'specifiers.MusicSpecifier([])'


def test_MusicSpecifier_format_02():
    r'''Empty. With keywords.
    '''

    specifier = scoremanagertools.specifiers.MusicSpecifier([], name='foo')

    assert repr(specifier) == "MusicSpecifier([], name='foo')"
    assert testtools.compare(
        specifier._storage_format,
        r'''
        specifiers.MusicSpecifier([],
            name='foo',
            )
        ''',
        )


def test_MusicSpecifier_format_03():
    r'''Populated. Without keywords.
    '''

    mcs_1 = scoremanagertools.specifiers.MusicContributionSpecifier([])
    mcs_1.append(specifiers.ArticulationSpecifier(articulation_handler_name='foo articulations'))

    mcs_2 = scoremanagertools.specifiers.MusicContributionSpecifier([])
    mcs_2.append(specifiers.ArticulationSpecifier(articulation_handler_name='bar articulations'))

    ms = scoremanagertools.specifiers.MusicSpecifier([mcs_1, mcs_2])

    assert testtools.compare(
        ms.storage_format,
        '''
        specifiers.MusicSpecifier([
            specifiers.MusicContributionSpecifier([
                specifiers.ArticulationSpecifier(
                    articulation_handler_name='foo articulations'
                    ),
                ]),
            specifiers.MusicContributionSpecifier([
                specifiers.ArticulationSpecifier(
                    articulation_handler_name='bar articulations'
                    ),
                ]),
            ])
        ''',
        )


def test_MusicSpecifier_format_04():
    r'''Populated. With keywords.
    '''

    mcs_1 = scoremanagertools.specifiers.MusicContributionSpecifier([])
    mcs_1.append(specifiers.ArticulationSpecifier(articulation_handler_name='foo articulations'))

    mcs_2 = scoremanagertools.specifiers.MusicContributionSpecifier([])
    mcs_2.append(specifiers.ArticulationSpecifier(articulation_handler_name='bar articulations'))

    ms = scoremanagertools.specifiers.MusicSpecifier([mcs_1, mcs_2], name='blue music')

    assert testtools.compare(
        ms.storage_format,
        '''
        specifiers.MusicSpecifier([
            specifiers.MusicContributionSpecifier([
                specifiers.ArticulationSpecifier(
                    articulation_handler_name='foo articulations'
                    ),
                ]),
            specifiers.MusicContributionSpecifier([
                specifiers.ArticulationSpecifier(
                    articulation_handler_name='bar articulations'
                    ),
                ]),
            ],
            name='blue music',
            )
        ''',
        )

    assert repr(ms) == "MusicSpecifier([MusicContributionSpecifier([ArticulationSpecifier(articulation_handler_name='foo articulations')]), MusicContributionSpecifier([ArticulationSpecifier(articulation_handler_name='bar articulations')])], name='blue music')"
