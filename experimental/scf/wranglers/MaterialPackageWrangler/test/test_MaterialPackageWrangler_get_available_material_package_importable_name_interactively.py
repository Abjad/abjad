import scf


def test_MaterialPackageWrangler_get_available_material_package_importable_name_interactively_01():

    wrangler = scf.wranglers.MaterialPackageWrangler()

    result = wrangler.get_available_material_package_importable_name_interactively(user_input='foo')
    assert result == 'materials.foo'

    result = wrangler.get_available_material_package_importable_name_interactively(user_input='red~notes q')
    assert result is None


def test_MaterialPackageWrangler_get_available_material_package_importable_name_interactively_02():

    wrangler = scf.wranglers.MaterialPackageWrangler()
    wrangler.session._current_score_package_short_name = 'betoerung'

    result = wrangler.get_available_material_package_importable_name_interactively(user_input='foo')
    assert result == 'betoerung.mus.materials.foo'

    result = wrangler.get_available_material_package_importable_name_interactively(user_input='speckled~time~token~maker q')
    assert result is None


def test_MaterialPackageWrangler_get_available_material_package_importable_name_interactively_03():

    wrangler = scf.wranglers.MaterialPackageWrangler()

    result = wrangler.get_available_material_package_importable_name_interactively(user_input='q')
    assert result is None

    result = wrangler.get_available_material_package_importable_name_interactively(user_input='b')
    assert result is None

    result = wrangler.get_available_material_package_importable_name_interactively(user_input='studio')
    assert result is None
