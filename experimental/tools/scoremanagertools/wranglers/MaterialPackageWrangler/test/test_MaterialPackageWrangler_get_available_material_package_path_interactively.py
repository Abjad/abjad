from experimental import *


def test_MaterialPackageWrangler_get_available_material_packagesystem_path_interactively_01():

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()

    result = wrangler.get_available_material_packagesystem_path_interactively(user_input='foo')
    assert result == 'experimental.tools.scoremanagertools.built_in_materials.foo'

    result = wrangler.get_available_material_packagesystem_path_interactively(user_input='red~notes q')
    assert result is None


def test_MaterialPackageWrangler_get_available_material_packagesystem_path_interactively_02():

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    wrangler._session._underscore_delimited_current_score_name = 'red_example_score'

    result = wrangler.get_available_material_packagesystem_path_interactively(user_input='foo')
    assert result == 'experimental.tools.scoremanagertools.built_in_scores.red_example_score.music.materials.foo'


def test_MaterialPackageWrangler_get_available_material_packagesystem_path_interactively_03():

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()

    result = wrangler.get_available_material_packagesystem_path_interactively(user_input='q')
    assert result is None

    result = wrangler.get_available_material_packagesystem_path_interactively(user_input='b')
    assert result is None

    result = wrangler.get_available_material_packagesystem_path_interactively(user_input='home')
    assert result is None
