from experimental.tools.scoremanagertools import specifiers
from experimental import *


def test_MusicContributionSpecifier_format_01():
    '''Empty.
    '''

    specifier = scoremanagertools.specifiers.MusicContributionSpecifier([])
    assert repr(specifier) == 'MusicContributionSpecifier([])'
    assert specifier._storage_format == 'specifiers.MusicContributionSpecifier([])'


def test_MusicContributionSpecifier_format_02():
    '''Populated.
    '''

    specifier = scoremanagertools.specifiers.MusicContributionSpecifier([])
    specifier.append(specifiers.ArticulationSpecifier(articulation_handler_name='foo articulations'))
    specifier.append(specifiers.ClefSpecifier(clef_name='treble'))
    specifier.append(specifiers.DirectiveSpecifier(directive_handler_name='foo directives'))

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
            )
        ])
    '''

    assert repr(specifier) == "MusicContributionSpecifier([ArticulationSpecifier(articulation_handler_name='foo articulations'), ClefSpecifier(clef_name='treble'), DirectiveSpecifier(directive_handler_name='foo directives')])"

    assert specifier._storage_format == "specifiers.MusicContributionSpecifier([\n\tspecifiers.ArticulationSpecifier(\n\t\tarticulation_handler_name='foo articulations'\n\t\t),\n\tspecifiers.ClefSpecifier(\n\t\tclef_name='treble'\n\t\t),\n\tspecifiers.DirectiveSpecifier(\n\t\tdirective_handler_name='foo directives'\n\t\t)\n\t])"
