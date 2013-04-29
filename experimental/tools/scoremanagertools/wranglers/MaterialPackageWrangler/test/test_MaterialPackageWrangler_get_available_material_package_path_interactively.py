from experimental import *


def test_MaterialPackageWrangler_get_available_material_package_path_interactively_01():

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()

    result = wrangler.get_available_material_package_path_interactively(user_input='foo')
    assert result == 'materials.foo'

    result = wrangler.get_available_material_package_path_interactively(user_input='red~notes q')
    assert result is None


def test_MaterialPackageWrangler_get_available_material_package_path_interactively_02():

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    wrangler.session._current_score_package_name = 'example_score_1'

    result = wrangler.get_available_material_package_path_interactively(user_input='foo')
    assert result == 'example_score_1.mus.materials.foo'


def test_MaterialPackageWrangler_get_available_material_package_path_interactively_03():

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()

    result = wrangler.get_available_material_package_path_interactively(user_input='q')
    assert result is None

    result = wrangler.get_available_material_package_path_interactively(user_input='b')
    assert result is None

    result = wrangler.get_available_material_package_path_interactively(user_input='home')
    assert result is None
