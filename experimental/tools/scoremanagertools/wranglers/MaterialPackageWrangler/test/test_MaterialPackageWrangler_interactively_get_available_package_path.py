# -*- encoding: utf-8 -*-
from experimental import *


def test_MaterialPackageWrangler_interactively_get_available_package_path_01():

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()

    result = wrangler.interactively_get_available_packagesystem_path(
        pending_user_input='foo')
    assert result == 'experimental.tools.scoremanagertools.materialpackages.foo'

    result = wrangler.interactively_get_available_packagesystem_path(
        pending_user_input='red~notes q')
    assert result is None


def test_MaterialPackageWrangler_interactively_get_available_package_path_02():

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    wrangler.session._snake_case_current_score_name = 'red_example_score'

    result = wrangler.interactively_get_available_packagesystem_path(
        pending_user_input='foo')
    assert result == 'experimental.tools.scoremanagertools.scorepackages.red_example_score.materials.foo'


def test_MaterialPackageWrangler_interactively_get_available_package_path_03():

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()

    result = wrangler.interactively_get_available_packagesystem_path(
        pending_user_input='q')
    assert result is None

    result = wrangler.interactively_get_available_packagesystem_path(
        pending_user_input='b')
    assert result is None

    result = wrangler.interactively_get_available_packagesystem_path(
        pending_user_input='home')
    assert result is None
