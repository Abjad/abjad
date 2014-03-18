# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_TargetManifest_change__to_initializer_argument_name_01():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.MarkupEditor(session=session)

    assert editor._target_manifest._to_initializer_argument_names(
        'contents_string') == 'arg'
    assert editor._target_manifest._to_initializer_argument_names(
        'direction') == 'direction'


def test_TargetManifest_change__to_initializer_argument_name_02():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.MarkupEditor(session=session)

    statement = "editor._target_manifest.change_retrievable_attribute_name"
    statement += "_to_initializer_argument_name('asdfasdf')"
    assert pytest.raises(Exception, statement)
