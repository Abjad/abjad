# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools import specifiers
from experimental import *


def test_MusicContributionSpecifier___format___01():
    r'''Empty.
    '''

    specifier = scoremanagertools.specifiers.MusicContributionSpecifier([])
    assert repr(specifier) == 'MusicContributionSpecifier([])'
    assert format(specifier) == 'specifiers.MusicContributionSpecifier([])'


def test_MusicContributionSpecifier___format___02():
    r'''Populated.
    '''

    specifier = scoremanagertools.specifiers.MusicContributionSpecifier([])
    specifier.append(specifiers.ArticulationSpecifier(articulation_handler_name='foo articulations'))
    specifier.append(specifiers.ClefSpecifier(clef_name='treble'))
    specifier.append(specifiers.DirectiveSpecifier(directive_handler_name='foo directives'))

    testtools.compare(
        format(specifier),
        '''
        specifiers.MusicContributionSpecifier([
            specifiers.ArticulationSpecifier(
                articulation_handler_name='foo articulations'
                ),
            specifiers.ClefSpecifier(
                clef_name='treble'
                ),
            specifiers.DirectiveSpecifier(
                directive_handler_name='foo directives'
                ),
            ])
        ''',
        )

    assert repr(specifier) == "MusicContributionSpecifier([ArticulationSpecifier(articulation_handler_name='foo articulations'), ClefSpecifier(clef_name='treble'), DirectiveSpecifier(directive_handler_name='foo directives')])"
