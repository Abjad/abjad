# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_get_available_package_path_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()

    result = wrangler.get_available_package_path(
        pending_user_input='foo')
    assert result == 'scoremanager.materialpackages.foo'

    result = wrangler.get_available_package_path(
        pending_user_input='example~notes q')
    assert result is None


def test_MaterialPackageWrangler_get_available_package_path_02():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    wrangler._session._current_score_snake_case_name = 'red_example_score'

    result = wrangler.get_available_package_path(
        pending_user_input='foo')
    string = 'red_example_score.materials.foo'
    assert result == string


def test_MaterialPackageWrangler_get_available_package_path_03():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()

    result = wrangler.get_available_package_path(
        pending_user_input='q')
    assert result is None

    result = wrangler.get_available_package_path(
        pending_user_input='b')
    assert result is None

    result = wrangler.get_available_package_path(
        pending_user_input='h')
    assert result is None
