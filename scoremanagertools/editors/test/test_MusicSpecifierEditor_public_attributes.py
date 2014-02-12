# -*- encoding: utf-8 -*-
from experimental import *


def test_MusicSpecifierEditor_public_attributes_01():
    r'''Without target.
    '''

    editor = scoremanagertools.editors.MusicSpecifierEditor()

    assert editor._breadcrumb == 'music specifier'
    assert not editor.has_target
    assert editor.target is None
    assert editor.target_attribute_tokens == [
        #('id', 'custom_identifier', 'None'),
        ]
    assert editor.target_name is None


def test_MusicSpecifierEditor_public_attributes_02():
    r'''With target.
    '''

    mcs_1 = scoremanagertools.specifiers.MusicContributionSpecifier([])
    mcs_1.articulation_specifier = 'foo'
    mcs_1.clef_specifier = 'bar'
    mcs_1.directive_specifier = ['apple', 'banana', 'cherry']

    mcs_2 = scoremanagertools.specifiers.MusicContributionSpecifier([])
    mcs_2.articulation_specifier = 'blee'
    mcs_2.clef_specifier = 'blah'
    mcs_2.directive_specifier = ['durian']

    ms = scoremanagertools.specifiers.MusicSpecifier([])
    ms.extend([mcs_1, mcs_2])

    r'''
    specifiers.MusicSpecifier([
        specifiers.MusicContributionSpecifier(
            articulation_specifier='foo',
            clef_specifier='bar',
            directive_specifier=['apple', 'banana', 'cherry']
            ),
        specifiers.MusicContributionSpecifier(
            articulation_specifier='blee',
            clef_specifier='blah',
            directive_specifier=['durian']
            )
        ],
        )
    '''

    editor = scoremanagertools.editors.MusicSpecifierEditor(target=ms)

    assert editor._breadcrumb == 'music specifier'
    assert editor.has_target
    assert editor.target is ms
    assert editor.target_attribute_tokens == [
        ]
    assert editor.target_name is None
