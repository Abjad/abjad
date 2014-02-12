# -*- encoding: utf-8 -*-
from experimental import *
from scoremanager import specifiers


def test_MusicContributionSpecifier___format___01():
    r'''Empty.
    '''

    specifier = scoremanager.specifiers.MusicContributionSpecifier([])
    assert repr(specifier) == 'MusicContributionSpecifier([])'
    assert systemtools.TestManager.compare(
        format(specifier),
        r'''
        specifiers.MusicContributionSpecifier(
            []
            )
        ''',
        )


def test_MusicContributionSpecifier___format___02():
    r'''Populated.
    '''

    specifier = scoremanager.specifiers.MusicContributionSpecifier([])
    specifier.append(specifiers.ArticulationSpecifier(articulation_handler_name='foo articulations'))
    specifier.append(specifiers.ClefSpecifier(clef_name='treble'))
    specifier.append(specifiers.DirectiveSpecifier(directive_handler_name='foo directives'))

    systemtools.TestManager.compare(
        format(specifier),
        '''
        specifiers.MusicContributionSpecifier(
            [
                specifiers.ArticulationSpecifier(
                    articulation_handler_name='foo articulations'
                    ),
                specifiers.ClefSpecifier(
                    clef_name='treble'
                    ),
                specifiers.DirectiveSpecifier(
                    directive_handler_name='foo directives'
                    ),
                ]
            )
        ''',
        )

    assert repr(specifier) == "MusicContributionSpecifier([ArticulationSpecifier(articulation_handler_name='foo articulations'), ClefSpecifier(clef_name='treble'), DirectiveSpecifier(directive_handler_name='foo directives')])"
