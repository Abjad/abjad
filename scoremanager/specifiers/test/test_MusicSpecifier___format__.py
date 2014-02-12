# -*- encoding: utf-8 -*-
from scoremanager import specifiers
from experimental import *


def test_MusicSpecifier___format___01():
    r'''Empty. No keywords.
    '''

    specifier = scoremanager.specifiers.MusicSpecifier([])

    assert repr(specifier) == 'MusicSpecifier([])'
    assert systemtools.TestManager.compare(
        format(specifier),
        r'''
        specifiers.MusicSpecifier(
            []
            )
        ''',
        )


def test_MusicSpecifier___format___02():
    r'''Empty. With keywords.
    '''

    specifier = scoremanager.specifiers.MusicSpecifier([], custom_identifier='foo')

    assert repr(specifier) == "MusicSpecifier([], custom_identifier='foo')"
    assert systemtools.TestManager.compare(
        format(specifier),
        r'''
        specifiers.MusicSpecifier(
            [],
            custom_identifier='foo',
            )
        ''',
        )


def test_MusicSpecifier___format___03():
    r'''Populated. Without keywords.
    '''

    mcs_1 = scoremanager.specifiers.MusicContributionSpecifier([])
    mcs_1.append(specifiers.ArticulationSpecifier(articulation_handler_name='foo articulations'))

    mcs_2 = scoremanager.specifiers.MusicContributionSpecifier([])
    mcs_2.append(specifiers.ArticulationSpecifier(articulation_handler_name='bar articulations'))

    ms = scoremanager.specifiers.MusicSpecifier([mcs_1, mcs_2])

    assert systemtools.TestManager.compare(
        format(ms),
        '''
        specifiers.MusicSpecifier(
            [
                specifiers.MusicContributionSpecifier(
                    [
                        specifiers.ArticulationSpecifier(
                            articulation_handler_name='foo articulations',
                            ),
                        ]
                    ),
                specifiers.MusicContributionSpecifier(
                    [
                        specifiers.ArticulationSpecifier(
                            articulation_handler_name='bar articulations',
                            ),
                        ]
                    ),
                ]
            )
        ''',
        )


def test_MusicSpecifier___format___04():
    r'''Populated. With keywords.
    '''

    mcs_1 = scoremanager.specifiers.MusicContributionSpecifier([])
    mcs_1.append(specifiers.ArticulationSpecifier(articulation_handler_name='foo articulations'))

    mcs_2 = scoremanager.specifiers.MusicContributionSpecifier([])
    mcs_2.append(specifiers.ArticulationSpecifier(articulation_handler_name='bar articulations'))

    ms = scoremanager.specifiers.MusicSpecifier([mcs_1, mcs_2], custom_identifier='blue music')

    assert systemtools.TestManager.compare(
        format(ms),
        '''
        specifiers.MusicSpecifier(
            [
                specifiers.MusicContributionSpecifier(
                    [
                        specifiers.ArticulationSpecifier(
                            articulation_handler_name='foo articulations',
                            ),
                        ]
                    ),
                specifiers.MusicContributionSpecifier(
                    [
                        specifiers.ArticulationSpecifier(
                            articulation_handler_name='bar articulations',
                            ),
                        ]
                    ),
                ],
            custom_identifier='blue music',
            )
        ''',
        )

    assert repr(ms) == "MusicSpecifier([MusicContributionSpecifier([ArticulationSpecifier(articulation_handler_name='foo articulations')]), MusicContributionSpecifier([ArticulationSpecifier(articulation_handler_name='bar articulations')])], custom_identifier='blue music')"
