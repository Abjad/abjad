import py
from experimental import *


def test_TargetManifest_change_initializer_argument_name_to_retrievable_attribute_name_01():

    editor = scoremanagertools.editors.MarkupEditor()

    assert editor.target_manifest.change_initializer_argument_name_to_retrievable_attribute_name('arg') == \
        'contents_string'

    assert editor.target_manifest.change_initializer_argument_name_to_retrievable_attribute_name('direction') == \
        'direction'


def test_TargetManifest_change_initializer_argument_name_to_retrievable_attribute_name_02():

    editor = scoremanagertools.editors.MarkupEditor()

    assert py.test.raises(Exception,
        "editor.target_manifest.change_initializer_argument_name_to_retrievable_attribute_name('asdfasdf')")
