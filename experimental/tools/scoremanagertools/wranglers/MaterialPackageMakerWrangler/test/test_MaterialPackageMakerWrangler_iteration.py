from experimental import *

score_manager = scoremanagertools.scoremanager.ScoreManager()
wrangler = score_manager.material_package_maker_wrangler


def test_MaterialPackageMakerWrangler_iteration_01():

    assert wrangler.list_score_internal_asset_package_paths() == []


def test_MaterialPackageMakerWrangler_iteration_02():

    assert wrangler.list_score_internal_asset_container_package_paths() == []


def test_MaterialPackageMakerWrangler_iteration_03():

    assert 'scoremanagertools.materialpackagemakers.PitchRangeInventoryMaterialPackageMaker' in \
        wrangler.list_asset_package_paths()


def test_MaterialPackageMakerWrangler_iteration_04():

    assert ('scoremanagertools.materialpackagemakers.PitchRangeInventoryMaterialPackageMaker',
        'pitch range inventory material package maker') in wrangler._make_visible_asset_menu_tokens()


def test_MaterialPackageMakerWrangler_iteration_05():

    assert 'pitch range inventory material package maker' in wrangler.list_space_delimited_lowercase_asset_names()
