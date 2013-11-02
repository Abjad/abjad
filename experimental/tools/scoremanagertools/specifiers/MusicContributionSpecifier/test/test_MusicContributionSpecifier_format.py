# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools import specifiers
from experimental import *


def test_MusicContributionSpecifier_format_01():
    r'''Empty.
    '''

    specifier = scoremanagertools.specifiers.MusicContributionSpecifier([])
    assert repr(specifier) == 'MusicContributionSpecifier([])'
    assert specifier._storage_format == 'specifiers.MusicContributionSpecifier([])'


def test_MusicContributionSpecifier_format_02():
    r'''Populated.
    '''

    specifier = scoremanagertools.specifiers.MusicContributionSpecifier([])
    specifier.append(specifiers.ArticulationSpecifier(articulation_handler_name='foo articulations'))
    specifier.append(specifiers.ClefSpecifier(clef_name='treble'))
    specifier.append(specifiers.DirectiveSpecifier(directive_handler_name='foo directives'))

    testtools.compare(
        specifier.storage_format,
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
