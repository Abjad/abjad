# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MusicSpecifierEditor_public_attributes_01():
    r'''Without target.
    '''

    editor = scoremanager.editors.MusicSpecifierEditor()

    assert editor._breadcrumb == 'music specifier'
    assert not editor.has_target
    assert editor.target is None
    assert editor.target_attribute_tokens == []
    assert editor.target_name is None


def test_MusicSpecifierEditor_public_attributes_02():
    r'''With target.
    '''

    specifier_1 = scoremanager.specifiers.MusicContributionSpecifier([])
    specifier_1.articulation_specifier = 'foo'
    specifier_1.clef_specifier = 'bar'
    specifier_1.directive_specifier = ['apple', 'banana', 'cherry']

    specifier_2 = scoremanager.specifiers.MusicContributionSpecifier([])
    specifier_2.articulation_specifier = 'blee'
    specifier_2.clef_specifier = 'blah'
    specifier_2.directive_specifier = ['durian']

    ms = scoremanager.specifiers.MusicSpecifier([])
    ms.extend([specifier_1, specifier_2])

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

    editor = scoremanager.editors.MusicSpecifierEditor(target=ms)

    assert editor._breadcrumb == 'music specifier'
    assert editor.has_target
    assert editor.target is ms
    assert editor.target_attribute_tokens == []
    assert editor.target_name is None
