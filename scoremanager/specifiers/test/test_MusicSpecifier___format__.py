# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
from scoremanager import specifiers


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

    specifier = scoremanager.specifiers.MusicSpecifier(
        [], 
        custom_identifier='foo',
        )

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

    specifier_1 = scoremanager.specifiers.MusicContributionSpecifier([])
    specifier_1.append(specifiers.ArticulationSpecifier(
        articulation_handler_name='foo articulations'))

    specifier_2 = scoremanager.specifiers.MusicContributionSpecifier([])
    specifier_2.append(specifiers.ArticulationSpecifier(
        articulation_handler_name='bar articulations'))

    specifier = scoremanager.specifiers.MusicSpecifier([specifier_1, specifier_2])

    assert systemtools.TestManager.compare(
        format(specifier),
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

    specifier_1 = scoremanager.specifiers.MusicContributionSpecifier([])
    specifier_1.append(specifiers.ArticulationSpecifier(
        articulation_handler_name='foo articulations'))

    specifier_2 = scoremanager.specifiers.MusicContributionSpecifier([])
    specifier_2.append(specifiers.ArticulationSpecifier(
        articulation_handler_name='bar articulations'))

    specifier = scoremanager.specifiers.MusicSpecifier(
        [specifier_1, specifier_2], 
        custom_identifier='blue music',
        )

    assert systemtools.TestManager.compare(
        format(specifier),
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

    assert repr(specifier) == "MusicSpecifier([MusicContributionSpecifier([ArticulationSpecifier(articulation_handler_name='foo articulations')]), MusicContributionSpecifier([ArticulationSpecifier(articulation_handler_name='bar articulations')])], custom_identifier='blue music')"
