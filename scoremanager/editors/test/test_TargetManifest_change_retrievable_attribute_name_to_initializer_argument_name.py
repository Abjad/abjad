# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_TargetManifest_change_retrievable_attribute_name_to_initializer_argument_name_01():

    editor = scoremanager.editors.MarkupEditor()

    assert editor.target_manifest.change_retrievable_attribute_name_to_initializer_argument_name(
        'contents_string') == 'arg'
    assert editor.target_manifest.change_retrievable_attribute_name_to_initializer_argument_name(
        'direction') == 'direction'


def test_TargetManifest_change_retrievable_attribute_name_to_initializer_argument_name_02():

    editor = scoremanager.editors.MarkupEditor()

    assert pytest.raises(Exception,
        "editor.target_manifest.change_retrievable_attribute_name_to_initializer_argument_name('asdfasdf')")
