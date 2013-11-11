# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools import specifiers
from experimental import *


def test_MusicSpecifier___format___01():
    r'''Empty. No keywords.
    '''

    specifier = scoremanagertools.specifiers.MusicSpecifier([])

    assert repr(specifier) == 'MusicSpecifier([])'
    assert format(specifier) == 'specifiers.MusicSpecifier([])'


def test_MusicSpecifier___format___02():
    r'''Empty. With keywords.
    '''

    specifier = scoremanagertools.specifiers.MusicSpecifier([], name='foo')

    assert repr(specifier) == "MusicSpecifier([], name='foo')"
    assert systemtools.TestManager.compare(
        format(specifier),
        r'''
        specifiers.MusicSpecifier([],
            name='foo',
            )
        ''',
        )


def test_MusicSpecifier___format___03():
    r'''Populated. Without keywords.
    '''

    mcs_1 = scoremanagertools.specifiers.MusicContributionSpecifier([])
    mcs_1.append(specifiers.ArticulationSpecifier(articulation_handler_name='foo articulations'))

    mcs_2 = scoremanagertools.specifiers.MusicContributionSpecifier([])
    mcs_2.append(specifiers.ArticulationSpecifier(articulation_handler_name='bar articulations'))

    ms = scoremanagertools.specifiers.MusicSpecifier([mcs_1, mcs_2])

    assert systemtools.TestManager.compare(
        format(ms),
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


def test_MusicSpecifier___format___04():
    r'''Populated. With keywords.
    '''

    mcs_1 = scoremanagertools.specifiers.MusicContributionSpecifier([])
    mcs_1.append(specifiers.ArticulationSpecifier(articulation_handler_name='foo articulations'))

    mcs_2 = scoremanagertools.specifiers.MusicContributionSpecifier([])
    mcs_2.append(specifiers.ArticulationSpecifier(articulation_handler_name='bar articulations'))

    ms = scoremanagertools.specifiers.MusicSpecifier([mcs_1, mcs_2], name='blue music')

    assert systemtools.TestManager.compare(
        format(ms),
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
